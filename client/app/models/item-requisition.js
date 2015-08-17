import DS from 'ember-data';

export default DS.Model.extend({
  item: DS.belongsTo('item'),
  checkedOutBy: DS.attr('string'),
  checkedOutOn: DS.attr('date'),
  checkedInOn: DS.attr('date'),
  lastModifiedOn: DS.attr('date')
});
