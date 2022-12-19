odoo.define("coupons_pos.coupons", function (require) {
    "use strict";
    var core = require('web.core');
    var pos_screen = require('point_of_sale.screens');
    var pos_model = require('point_of_sale.models');
    var pos_popup = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var models = pos_model.PosModel.prototype.models;
    var _t = core._t;

    function find_coupon(code, coupons) {
        var coupon = [];
        for(var i in coupons){
            if (coupons[i]['code'] == code){
                coupon.push(coupons[i]);
            }
        }
        return (coupon.length > 0) ? coupon : false; 
    }

    function check_expiry(expiry_date) {
        var today = moment().format('YYYY-MM-DD');
        return (today < expiry_date) ? true : false;
    }

    function get_coupon_product(products) {
        for (var i in products){
            if(products[i]['display_name'] == 'Gift-Coupon')
                return products[i]['id'];
        }
        return false;
    }

    models.push({
        model: 'coupon.pos',
        fields: ['id', 'name', 'code', 'expiry_date', 'disc_amount'],
        loaded: function (self, coupons) {
            self.coupons = coupons;
        }
    });

    var CouponWidget = pos_screen.ActionButtonWidget.extend({
        template:"CouponWidget",
        init: function(parent) {
            return this._super(parent);
        },
        renderElement: function () {
            var self = this;
            this._super();
            this.$(".coupons").click( function () {
                self.gui.show_popup('coupon', {
                    'title': _t('Enter Your Coupon'),
                });
            });
        }
    });

    pos_screen.ProductScreenWidget.include({
        start: function () {
            this._super();
            this.coupons = new CouponWidget(this, {});
            this.coupons.replace(this.$('.placeholder-CouponWidget'));
        }
    });

    var CouponPopupWidget = pos_popup.extend({
        template: 'CouponPopupWidget',
        init: function(parent) {
            this.coupon_product = null;
            return this._super(parent);
        },
        show: function(options){
            options = options || {};
            this._super(options);
            if(!this.coupon_product)
                this.coupon_product = get_coupon_product(this.pos.db.product_by_id);
            this.renderElement();
            this.$('input').focus();
        },
        click_confirm: function(){
            var value = this.$('input').val();
            this.gui.close_popup();
            if( this.options.confirm ){
                this.options.confirm.call(this, value);
            }
        },
        renderElement: function () {
            this._super();
            var self = this;

            this.$(".validate_coupon").click(function () {
                var current_order = self.pos.get_order();
                var coupon = $(".coupon_code").val();
                
                if (current_order.orderlines.models.length == 0){
                    self.gui.show_popup('error', {
                        'title': _t("No products !"),
                        'body': _t("You cannot apply coupon without products"),
                    });
                } else if (coupon) {
                    var coupon_res = find_coupon(coupon, self.pos.coupons);
                    if (coupon_res) {
                        if (check_expiry(coupon_res[0]['expiry_date']) ) {
                            self.discount = coupon_res[0]['disc_amount'];
                            $(".confirm-coupon").css("display", "block");
                        } else {
                            self.gui.show_popup('error',{
                                'title': _t('Unable to apply Coupon !'),
                                'body': _t('You cannot use this coupon. Coupon has exceeded expiration date.'),
                            });
                        }
                    } else {
                        self.gui.show_popup('error',{
                            'title': _t('Unable to apply Coupon !'),
                            'body': _t('the coupon you entered is incorrect or does not exist.'),
                        });
                    }
                } 
            });

            this.$(".confirm-coupon").click(function () {
                var order = self.pos.get_order();
                var product = self.pos.db.get_product_by_id(self.coupon_product);
                var price = self.discount * -1;
                if (order.get_total_with_tax() - self.discount < 0) {
                    self.gui.show_popup('error', {
                        'title': _t('Unable to apply Coupon !'),
                        'body': _t('Coupon amount is too large to apply. The total amount cannot be negative'),
                    });
                } else {
                    order.add_product(product, {quantity: 1, price: price}); 
                    self.gui.close_popup();
                    self.gui.show_popup('alert',{
                        'title': _t('Successfully'),
                        'body': _t('Coupon has been activated'),
                    });
                }
            });
        }
    });

    gui.define_popup({name:'coupon', widget: CouponPopupWidget});
});