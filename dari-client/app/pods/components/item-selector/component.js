import Ember from 'ember';

export default Ember.Component.extend({
  selectedItems: [],

  actions: {
    select: function(item) {
      console.log('SELECTING');
      var items = this.get('selectedItems');
      if (items.contains(item)) {
        item.set('isChecked', false);
        items.removeObject(item);
      } else {
        item.set('isChecked', true);
        items.addObject(item);
      }
    }
  }
});
