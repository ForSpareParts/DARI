import Ember from 'ember';

export default Ember.Controller.extend({

  items: function() {
    return this.store.query('item', {current_qty: 1});
  }.property(),

  actions: {
    checkout: function(selectedItems) {
      var promises = [];
      selectedItems.forEach((item) => {
        var itemReq = this.store.createRecord('item-requisition', {
          item: item,
          checkedOutBy: this.get('model.username'),
        });
        promises.push(itemReq.save());
      });
      if (promises.length) {
        Ember.RSVP.all(promises)
        .then(() => {
          var alert = this.get('model');
          return new Ember.RSVP.Promise((resolve, reject) => {
            Ember.$.ajax({
              url: this.namespace + '/alerts/' + alert.get('id'),
              type: "PATCH",
              data: JSON.stringify({cleared: 1}),
              headers: this.headers
            })
            .done((data, textStatus, jqXHR) => {
              resolve(this.get('model').store.push('alerts', data['alerts']));
            })
            .fail((jqXHR, textStatus, errorThrown) => reject(errorThrown));
          });
        });
      }
    }
  }
});
