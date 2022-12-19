odoo.define("pos_promotions.promotions", function (require) {
    "use strict";
    var core = require('web.core');
    var pos_screen = require('point_of_sale.screens');
    var pos_model = require('point_of_sale.models');
    var models = pos_model.PosModel.prototype.models;
    var QWeb = core.qweb;
    var _t = core._t;

    function getResultCondition(condition) {
        if (condition['gift_type'] == 'discount') {
            return {
                'active': true,
                'type': 'discount',
                'disc_amount': condition['disc_amount']
            }; 
        } else {
            return {
                'active': true,
                'type': 'specific_product',
                'product': condition['product_id'],
                'amount': condition['amount']
            };                         
        }
    }

    function check_new_customer(promotions, partner_selected, partner_list) {
        var result;
        var is_new_customer = !partner_list.find(partner => partner['partner_id'][0] == partner_selected.id);
        var condition_new_customer = promotions.find(promo => promo['condition'] == 'new_customer');

        if (is_new_customer && condition_new_customer) {
            result = getResultCondition(condition_new_customer);
            localStorage.setItem("current_gift", JSON.stringify(result)); 
            return result;
        } 

        return {'active': false};

    }

    function check_specific_date(self, order, promotions) {
        var today = moment().format('YYYY-MM-DD'); 
        var result;
        var condition_specific_date = promotions.find(promo => promo['condition'] == 'specific_date');
        var spec_is_today = (today == condition_specific_date['spec_date']);

        if (condition_specific_date && spec_is_today) {
            result = getResultCondition(condition_specific_date);
            insertGiftIntoOrderline(self, order, result);
            return result;
        }

        return {'active': false};
    }

    function check_minimum_amount(self, order, promotions) {
        var result ;
        var condition_minimum_amount = promotions.find(promo => promo['condition'] == 'minimum_amount');
        var grather_than_min_amount = order.get_total_with_tax() >= condition_minimum_amount['min_amount'];

        if (condition_minimum_amount && grather_than_min_amount) {
            result = getResultCondition(condition_minimum_amount);
            insertGiftIntoOrderline(self, order, result);
            return result;
        }

        return {'active': false};

    }

    function get_discount_product(products) {
        for (var i in products){
            if(products[i]['display_name'] == 'Discount')
                return products[i]['id'];
        }

        return false;
    }

    function deletePromoFromOrderline(order, product) {
        var i = 0;
        while ( i < order.orderlines.models.length ) {
            if (order.orderlines.models[i].product === product) {
                order.remove_orderline(order.orderlines.models[i]);
            } else {
                i++;
            }
        }
    }

    function insertGiftIntoOrderline(self, order, condition) {
        if (condition.active) {
            if (condition.type == 'discount') {
                var disc_product = self.pos.db.get_product_by_id(get_discount_product(self.pos.db.product_by_id));
                deletePromoFromOrderline(order, disc_product);

                var price = condition.disc_amount * -1;
                if (order.get_total_with_tax() - self.discount < 0) {
                    price = 0;
                }
                order.add_product(disc_product, {quantity: 1, price: price}); 
            } else {
                var gift_product = self.pos.db.get_product_by_id(condition.product[0]);
                deletePromoFromOrderline(order, gift_product);

                var price = 0;

                order.add_product(gift_product, {quantity: condition.amount, price: price});
            
            }
        }
    }

    function checkAllConditions(self) {
        var order = self.pos.get_order();
        check_specific_date(self, order, self.pos.promotions);
        check_minimum_amount(self, order, self.pos.promotions);

        if (self.pos.get_order().get_client()) {
            var new_customer = check_new_customer(self.pos.promotions, self.pos.get_order().get_client(), self.pos.pos_order);
            insertGiftIntoOrderline(self, order, new_customer);
        } 
    }

    models.push(
        {
            model: 'promotions.pos',
            fields: ['condition', 'gift_type', 'amount', 'product_id', 'disc_amount', 'spec_date', 'min_amount'],
            loaded: function (self, promotions) {
                self.promotions = promotions;
            }
        },
        {
            model: 'pos.order',
            fields: ['partner_id'],
            loaded: function (self, pos_order) {
                self.pos_order = pos_order;
            }
        },
        {
            model: 'product.template',
            fields: ['id', 'is_promo'],
            loaded: function (self, product_template) {
                self.product_template = product_template;
            }
        },
    );

    

    pos_screen.ActionpadWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            this.$(".pay").click( function () {
                checkAllConditions(self);
            });
        }
    });

    pos_screen.ClientListScreenWidget.include ({
        show: function () {
            var self = this;
            this._super();

            this.$('.next').click(function(){
                var order = self.pos.get_order();
                var partner = $('.client-list-contents .highlight').data('id');
                var new_customer = check_new_customer(self.pos.promotions, self.pos.db.get_partner_by_id(partner), self.pos.pos_order);
                
                if (this.classList.contains('open_')) {
                    checkAllConditions(self);

                } else if (this.classList.contains('change_')) {
                    // change customer
                    if (new_customer.active) {
                        // new customer
                        checkAllConditions(self);
                    } else {
                        // old customer
                        var product;
                        var item = JSON.parse(localStorage.getItem("current_gift"));
                        if (item.type == 'discount') {
                            product = self.pos.db.get_product_by_id(get_discount_product(self.pos.db.product_by_id));
                        } else {    
                            product = self.pos.db.get_product_by_id(item.product[0]);
                        }
                        deletePromoFromOrderline(order, product);
                        checkAllConditions(self);
                    }
                } else {
                    // deselect
                    var product;

                    if (new_customer.active) {
                        if (new_customer.type == 'discount') {
                            product = self.pos.db.get_product_by_id(get_discount_product(self.pos.db.product_by_id));
                        } else {
                            product = self.pos.db.get_product_by_id(new_customer.product[0]);
                        }
                    }
                    deletePromoFromOrderline(order, product);
                    checkAllConditions(self);
                }

            });         
        },
        toggle_save_button: function(){
            var $button = this.$('.button.next');
            $button.removeClass('open_');
            $button.removeClass('change_');

            if (this.editing_client) {
                $button.addClass('oe_hidden');
                return;
            } else if( this.new_client ){
                if( !this.old_client){
                    $button.text(_t('Set Customer'));
                    $button.addClass('open_');
                }else{
                    $button.text(_t('Change Customer'));
                    $button.addClass('change_');
                }
            }else{
                $button.text(_t('Deselect Customer'));
            }
            $button.toggleClass('oe_hidden',!this.has_client_changed());
        },
    });

    pos_screen.PaymentScreenWidget.include({
        render_promotions: function () {
            var self  = this;
            var product_tmpl = self.pos.product_template;
            var order = this.pos.get_order();
            if (!order) {
                return;
            }

            checkAllConditions(self);

            var tmpl_id = [];
            for (var i in product_tmpl) {
                if (product_tmpl[i].is_promo == true) {
                    tmpl_id.push(product_tmpl[i].id);
                }
            }
            
            var promotions = [];
            var i = 0;
            while ( i < order.orderlines.models.length ) {
                if (tmpl_id.includes(order.orderlines.models[i].product.product_tmpl_id)) {
                    promotions.push({
                    'display_name': order.orderlines.models[i].product.display_name,
                    'quantity': order.orderlines.models[i].quantityStr,
                    'price': order.orderlines.models[i].price,
                   });
                } 
                i++;
            }
            this.$('.promotions-container').empty();
            
            if (promotions.length > 0) {
                this.$('.promotions-container').css("display", "block");

                var lines = $(QWeb.render('PaymentScreen-Promotions', 
                { 
                    widget:this,
                    promotions: promotions, 
                }
                ));
                
                lines.appendTo(this.$('.promotions-container'));
            } else {
                this.$('.promotions-container').css("display", "none");
            }
        },
        renderElement: function () {
            this._super();
            this.render_promotions();
        },
        show: function () {
            this._super();
            this.render_promotions();
        }
    });

    pos_screen.ProductScreenWidget.include({
        click_product: function(product) {
            if(product.to_weight && this.pos.config.iface_electronic_scale){
                this.gui.show_screen('scale',{product: product});
            }else{
                this.pos.get_order().add_product(product);
                checkAllConditions(this);
            }
         },
    });

    pos_screen.ProductListWidget.include({
        renderElement: function() {
            this._super();
            
            var product_tmpl = this.pos.product_template;
            var tmpl_id = [];
            for (var i in product_tmpl) {
                if (product_tmpl[i].is_promo == false) {
                    tmpl_id.push(product_tmpl[i].id);
                }
            }
            var list_container = this.el.querySelector('.product-list');
           
            var i = 0;
            while ( i < this.product_list.length ) {
                if (tmpl_id.includes(this.product_list[i].product_tmpl_id)) {
                    var product_node = this.render_product(this.product_list[i]);
                    list_container.appendChild(product_node);
                } 
                i++;
            }
            for (var i = 0; i < this.product_list.length - tmpl_id.length; i++) {
                $('article.product').eq(i).hide()
            }

        }
    });

});