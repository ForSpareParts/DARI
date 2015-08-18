/**
 * Initializes an alert list on the element indicated by the selector.
 *
 * The selector should point to the wrapping .alert-menu div for the alert list.
 */
var AlertList = function(selector) {
  this.container = $(selector);
  this.list = this.container.filter('ul');
  this.template = this.list.filter('li.template');

  this.command = this.container.data('command');
  this.inProgressAjax = null;
};

/**
 * Begins a polling request. This will result in continuous polling.
 * @return {[type]} [description]
 */
AlertList.prototype.startPoll = function() {
  var _this = this;

  if (this.inProgressAjax) {
    //we're already in the middle of a poll!
    return this.inProgressAjax;
  }

  var ajaxSettings = {
    dataType: 'json',
    method: 'get',

    error: this.ajaxError,
    success: this.handleAjax
  };

  this.inProgressAjax = $.ajax(
    SOME_URL + '?active=1&type=' + this.command,
    ajaxSettings);

  return this.inProgressAjax
};

AlertList.prototype.ajaxError = function() {
  return this.startPoll();
};

AlertList.prototype.handleAjax = function(data, textStatus, jqXHR) {
  this.inProgressAjax = null;
  this.render(data);

  return this.startPoll();
};

/**
 * Eliminate all visible alerts from the view.
 */
AlertList.prototype.clearView = function() {
  this.list.filter('li').not('.template').remove();
};

/**
 * Given an array of alert objects, update the view to reflect them.
 */
AlertList.prototype.render = function(alertArray) {
  var _this = this;
  this.clearView();

  alertArray.forEach(function(alertJSON) {
    var alertElement = this.createAlertElement(alertJSON);
    this.list.append(alertElement);
  });
};

AlertList.prototype.createAlertElement = function(alertJSON) {
  var cloned = this.template.clone();
  cloned.removeClass('template');

  cloned.data('alert-id', alertJSON.id);

  //update the link in the template to point at this specific alert
  var link = cloned.find('a');
  link.attr('href', link.attr('href') + '/' + alertJSON.id);

  cloned.find('.username').html(alertJSON.username);
  cloned.find('.text').html(alertJSON.text);

  return cloned;
};
