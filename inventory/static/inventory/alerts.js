/**
 * Initializes an alert list on the element indicated by the selector.
 *
 * The selector should point to the wrapping .alert-menu div for the alert list.
 */
var AlertList = function(selector) {
  this.container = $(selector);
  this.list = this.container.find('ul');
  this.template = this.list.find('li.template');

  this.command = this.container.data('command');
  this.alertApiURL = this.container.data('alert-api-url');
  this.cacheKey = 'alert-list-cache-' + this.command;
  this.inProgressAjax = null;

  //see if we've got anything to render from a previous page load
  var cache = this.getCache();
  if (cache) {
    this.render(cache);
  }
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

    error: this.ajaxError.bind(this),
    success: this.handleAjax.bind(this)
  };

  this.inProgressAjax = $.ajax(
    this.alertApiURL + '?active=1&type=' + this.command,
    ajaxSettings);

  return this.inProgressAjax
};

AlertList.prototype.ajaxError = function() {
  return this.startPoll();
};

AlertList.prototype.handleAjax = function(data, textStatus, jqXHR) {
  this.inProgressAjax = null;
  this.setCache(data);
  this.render(data);

  //delay the next poll for a few seconds
  setTimeout(this.startPoll.bind(this), 5000);
};

/**
 * Store a snapshot of this list's alerts in a localStorage cache.
 */
AlertList.prototype.setCache = function(data) {
  localStorage.setItem(this.cacheKey, JSON.stringify(data));
}

/**
 * Retrieve a snapshot of this list's alerts from a localStorage cache.
 */
AlertList.prototype.getCache = function() {
  var cachedString = localStorage.getItem(this.cacheKey);

  if (cachedString) {
    return JSON.parse(cachedString);
  }

  return null;
}

/**
 * Eliminate all visible alerts from the view.
 */
AlertList.prototype.clearView = function() {
  this.list.find('li').not('.template').remove();
};

/**
 * Given an array of alert objects, update the view to reflect them.
 */
AlertList.prototype.render = function(alertArray) {
  var _this = this;
  this.clearView();

  alertArray.forEach(function(alertJSON) {
    var alertElement = _this.createAlertElement(alertJSON);
    _this.list.append(alertElement);
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

$(function() {
  var en = new AlertList('#en-alerts');
  var er = new AlertList('#er-alerts');

  en.startPoll();
  er.startPoll();
});