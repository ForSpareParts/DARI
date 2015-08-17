import DS from 'ember-data';

export default DS.Model.extend({
  location: DS.attr('string'),
  category: DS.attr('string'),
  name: DS.attr('string'),
  materialNumber: DS.attr('string'),
  serialNumber: DS.attr('string'),
  kit: DS.attr('string'),
  notes: DS.attr('string'),
  sortByName: DS.attr('string'),
  shipment: DS.attr('string'),
  manual: DS.attr('string'),
  qtyAtInventory: DS.attr('number'),
  inventoryLoadedOn: DS.attr('date'),
  lastModifiedOn: DS.attr('date'),
  currentQty: DS.attr('number'),
  supercededBy: DS.belongsTo('item', {async: true})
});
