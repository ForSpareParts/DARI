import DS from 'ember-data';

export default DS.Model.extend({
  username: DS.attr('string'),
  type: DS.attr('string'),
  text: DS.attr('string'),
  setOn: DS.attr('date'),
  alertOn: DS.attr('date'),
  clearedOn: DS.attr('date')
});
