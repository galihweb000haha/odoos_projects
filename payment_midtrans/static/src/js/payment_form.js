odoo.define('payment_midtrans.payment_form', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var PaymentForm = require('payment.payment_form');
    
    PaymentForm.include({
        loadSnapUrl: function (acquirerId) {
            this._rpc({
                model: 'payment.acquirer',
                method: 'get_payment_acquirer_state',
                args: [parseInt(acquirerId)]
            }).then(function (result) {
                if (result == 'enabled') {
                    return ajax.loadJS("https://app.midtrans.com/snap/snap.js");
                } else {
                    return ajax.loadJS("https://app.sandbox.midtrans.com/snap/snap.js");
                }
            });
        },
        /**
         * @override
         */
        willStart: function () {
            var acquirerId;
            var self = this;

            return this._super.apply(this, arguments).then(function () {
                $('.o_payment_acquirer_select').on('click', function(e) {
                    acquirerId = this.querySelector('input[type="radio"]').dataset.acquirerId;
                    self.loadSnapUrl(acquirerId);
                });

                $.each($('.o_payment_acquirer_select').find('input'), function(index, value) {
                    if (value.checked) {
                        acquirerId = value.dataset.acquirerId;
                        self.loadSnapUrl(acquirerId);
                    }
                });
            });

        },
        /**
         * @override
         */
        payEvent: function (ev) {
            var self = this;
            this._super.apply(this, arguments).then( (values) => {
                var $checkedRadio = this.$('input[type="radio"]:checked');
                
                if ($checkedRadio.length === 1 && this.isFormPaymentRadio($checkedRadio) && $checkedRadio.data('provider') === 'midtrans') {
                    self._rpc({
                        model: 'payment.transaction',
                        method: 'payment_midtrans_transaction',
                        args: [[]]
                    }).then(function(result) {
                        var token = result.token;
                        
                        snap.pay(token, {
                            onSuccess: function(){ 
                                window.location = '/shop/confirmation';
                            },
                            onPending: function(){
                                self.do_warn('Warning', 'Wating your payment!');
                                window.location = '/shop/confirmation';
                            },
                            onError: function(){
                                self.do_warn('Error', 'Payment Failed!');
                                window.location = '/shop/confirmation';
                            },
                            onClose: function(){
                                self.do_warn('Warning', 'You closed the popup without finishing the payment');
                                window.location = '/shop/payment';
                            }
                        });
        
                    });
                }        
            }); 
        },

    });

});

