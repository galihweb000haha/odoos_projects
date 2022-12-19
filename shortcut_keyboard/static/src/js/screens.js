odoo.define('shortcut_keyboard.screens', function(require) {
    "use strict";

    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');

    var models = require('point_of_sale.models');

    screens.ProductScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options);

            var self = this;

            this.product_screen_keydown_event_handler = function(event) {

                if ( !$(document).find(".search-input").is(":focus") && !$(document).find(".product-screen").hasClass("oe_hidden") ) {
                    if (event.which == 81) {
                        self.gui.show_screen('clientlist');
                    }
                }

            }

            $(document).find("body").on('keydown', this.product_screen_keydown_event_handler);
        },

    });

    var _super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var self = this;
            models.load_fields('pos.payment.method',['shortcut']);
            _super_posmodel.initialize.apply(this, [session, attributes]);
        },
    })
    
   screens.PaymentScreenWidget.include({
       _init: function (parent, options) {
           this._super(parent, options);

           var self = this;

           this.payment_methods_keydown_event_handler = function (event) {
               event.preventDefault();
               if (!$($(document).find("div.payment-screen")[0]).hasClass('oe_hidden')) {
                   var payment_methods_ids = [];
                   self.pos.payment_methods.forEach(function (index) {
                       payment_methods_ids.push(index.id);
                   });

                   self._rpc({
                       model: 'account.journal',
                       method: 'get_shortcut_code',
                       args: [[], payment_methods_ids]
                   }).then(function (result) {
                       for (let [i,v] of result.ids.entries()) {
                           if (event.which == result.code[i]) {
                                self.click_paymentmethods(v);
                           }
                       }
                   });
                   // [IMP] Esc to trigger back button
                   if (event.which == 27) {
                       $($(document).find("div.payment-screen")[0]).find("div.top-content span.back").trigger('click');
                   }
               }
           };
           $(document).find("body").on('keydown', this.payment_methods_keydown_event_handler);
       },
   });

});