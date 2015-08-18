import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('checkout', {path: 'checkout/:id'});
  this.route('checkin', {path: 'checkin/:id'});
  this.route('item-requisitions');
});

export default Router;
