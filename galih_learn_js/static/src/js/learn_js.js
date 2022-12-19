odoo.define('galih_learn_js.learn_js', function(require) {
    var AbstractField = require('web.AbstractField');
    var FieldRegsitry = require('web.field_registry');

    var core = require('web.core');
    var qweb = core.qweb;

    var fields_utils = require('web.field_utils');
    var view_dialogs = require('web.view_dialogs');


    var WidgetOne = AbstractField.extend({
        step: 1,
        template: 'WidgetOneTemplate',
        events: {
            'click .btn-minus': 'btn_minus_action',
            'click .btn-plus': 'btn_plus_action',
            'click .btn-dollar': 'btn_dollar_action'
        },
        init: function() {
            this._super.apply(this, arguments);
            if (this.nodeOptions.step) {
                this.step = this.nodeOptions.step;
            } 
        },
        btn_minus_action: function() {
            var new_value = this.value - this.step;
            this._setValue(new_value.toString());
        },
        btn_plus_action: function() {
            var new_value = this.value + this.step;
            this._setValue(new_value.toString());
        },
        btn_dollar_action: function(){
            var self = this;
            new view_dialogs.SelectCreateDialog(this, {
                res_model: 'sale.order',
                title: "Pilih Sale Order",
                domain: [['state', '!=', 'draft']],
                no_create: true,
                on_selected: function (records) {
                    var record_ids = records.map(function(item){
                        return item['id'];
                    });
                    self._rpc({
                        model: self.attrs.relatedModel,
                        method: self.attrs.modifiers.relatedAction,
                        args: [record_ids]
                    }).then(function(result) {
                        self._setValue(result.toString());
                    });
                }
            }).open();
        },
        _render: function() {
            var self = this;
            var formated_value = fields_utils.format[this.formatType](this.value);
            this.$el.html($(qweb.render(this.template, {'widget': this, 'formated_value': formated_value})));
            this.$el.find('.btn-copy').click(function() {
                var field_one_val = self.value;
                var field_two_val = $('[name=field_two]').val();
                var field_three_val = field_one_val + parseInt(field_two_val);
                self.trigger_up('field_changed', {
                    dataPointID: self.dataPointID,
                    viewType: self.viewType,
                    changes: {'field_three': field_three_val},
                });
            })
        }
    });

    FieldRegsitry.add('widget_one', WidgetOne);
    return WidgetOne;
})