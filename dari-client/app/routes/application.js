import Ember from 'ember';

export default Ember.Route.extend({
  model: function(params) {
    var needs = this.store.query('alert', {active: 1, type: 'en'});
    var returns = this.store.query('alert', {active: 1, type: 'er'});
    return Ember.RSVP.all([needs, returns])
    .then((promises) => {
      return {
        needs: promises[0],
        returns: promises[1]
      };
    });
  }
});
