odoo.define('pos_basic.galih_custom_screens', function(require) {
    "use strict";

    var Screens = require('point_of_sale.screens');
    var OrderWidget = Screens.OrderWidget;

    var core = require('web.core');
    var _t = core._t;

    var QWeb = core.qweb;

    var chrome = require('point_of_sale.chrome');
    var OrderSelectorWidget = chrome.OrderSelectorWidget;


    OrderWidget.include({
        render_orderline: function (orderline) {

            var el_str  = QWeb.render('Orderline',{widget:this, line:orderline}); 
            var el_node = document.createElement('div');
                el_node.innerHTML = _.str.trim(el_str);
                el_node = el_node.childNodes[0];
                el_node.orderline = orderline;
                el_node.addEventListener('click',this.line_click_handler);
            var el_lot_icon = el_node.querySelector('.line-lot-icon');
            if(el_lot_icon){
                el_lot_icon.addEventListener('click', (function() {
                    this.show_product_lot(orderline);
                }.bind(this)));
            }

            orderline.node = el_node;
            el_node.innerHTML = `<img src="http://localhost:8010/web/image?model=product.product&field=image_128&id=${orderline.product.id}" style="width: 50px;display:inline-block;"> <div class="detail-order" style="display:inline-block;width:300px">` + el_node.innerHTML + `</div>`;

            return el_node;
        },

    });

    var ResetButton = Screens.ActionButtonWidget.extend({
        template: 'ResetButton',
        init: function (parent, options) {
            this._super(parent, options);
        },
        renderElement: function(){
            var self = this;
            this._super();
            this.$el.click(function(){
                self.button_click();
            });
        },
        button_click: function () {            
            var self  = this;
            var order = this.pos.get_order(); 
            if (!order) {
                return;
            } else if ( !order.is_empty() ){
                this.gui.show_popup('confirm',{
                    'title': _t('Destroy Current Order ?'),
                    'body': _t('You will lose any data associated with the current order'),
                    confirm: function(){
                        self.pos.delete_current_order();
                    },
                });
            } else {
                this.pos.delete_current_order();
            }
        },

    });

    Screens.define_action_button({
        'name': 'ResetButton',
        'widget': ResetButton,
        'condition': function(){
            return true;
        }
    });

    return {
        ResetButton: ResetButton,
    };


})