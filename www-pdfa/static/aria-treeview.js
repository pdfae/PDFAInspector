var g_focusHandled = false; // set to true if focus is handled

//
// Function resetFocusFlag() is a callback to reset the focusHandled flag. This is
// called by the timer set in the treeview focus handler
//
function resetFocusFlag() {
  g_focusHandled = false;
}

$(document).ready(function() {

  var treeviewApp = new treeview('tree1');

}); // end ready

//
// Function keyCodes() is an object to define keycodes for the application
//
function keyCodes() {

  this.enter      = 13;
  this.space      = 32;

  this.pageup     = 33;
  this.pagedown   = 34;
  this.end        = 35;
  this.home       = 36;
  this.left       = 37;
  this.up         = 38;
  this.right      = 39;
  this.down       = 40;
  this.asterisk   = 106;

} // end keyCodes()

//
// Function treeview() is a class constructor for a treeview widget. The widget binds to an
// unordered list. The top-level <ul> must have role='tree'. All list items must have role='treeitem'.
//
// Tree groups must be embedded lists within the listitem that heads the group. the top <ul> of a group
// must have role='group'. aria-expanded is used to indicate whether a group is expanded or collapsed. This
// property must be set on the listitem the encapsulates the group.
//
// @param (treeID string) treeID is the html id of the top-level <ul> of the list to bind the widget to
//
// @return N/A
//
function treeview(treeID) {

  // define the object properties
  this.$id = $('#' + treeID);
  this.$listitems = this.$id.find('li'); // an array of list items
  this.$groups = undefined; // an array of the listitems that function as group headers
  this.$visibleItems = undefined; // an array of currently visible listitems (including headers)
  this.focusHandled = false; // Set to true when a focus event is handled and reset after a small delay

  this.keys = new keyCodes();

  // initialize the treeview
  this.init();

  // bind event handlers
  this.bindHandlers();

} // end treeview() constructor

//
// Function init() is a member function to initialize the treeview widget. It traverses the tree, identifying
// which listitems are headers for groups and applying initial collapsed are expanded styling
//
// @return N/A
//
treeview.prototype.init = function() {

  var thisObj = this;

  // iterate through the tree and apply the groupHeader class and styling to the group headers
  this.$id.find('li').each (function(index) {

    var $group = $(this).children('ul');

    if ($group.length > 0) {
      // this listitem is a group header

      // Apply the group header styling
      $(this).addClass('groupHeader');

      // insert the header image. Note: this method allows the widget to degrade gracefully
      // if javascript is disabled or there is some other error.
      $(this).prepend('<img class="headerImg" src="images/treeExpanded.gif" />');

      // If the aria-expanded is false, hide the group and display the collapsed state image
      if ($(this).attr('aria-expanded') == 'false') {
        $group.hide();
        $(this).find('img').attr('src', 'images/treeContracted.gif');
      }
    }
  });

  // create the group and initial visible item array
  this.$groups = $('li.groupHeader');
  this.$visibleItems = this.$id.find('li:visible');

} // end init()

//
// Function expandGroup() is a member function to expand a collapsed group
//
// @param($id object) $id is the jquery id of the group header of the group to expand
//
// @param(focus boolean) focus is true if the group header has focus, false otherwise
//
// @return N/A
//
treeview.prototype.expandGroup = function($id, focus) {

  var $group = $id.children('ul');

  // expand the group
  $group.show();

  $id.attr('aria-expanded', 'true');

  if (focus == true) {
    $id.children('img').attr('src', 'images/treeExpandedFocus.gif');
  }
  else {
    $id.children('img').attr('src', 'images/treeExpanded.gif');
  }

  // refresh the list of visible items
  this.$visibleItems = this.$id.find('li:visible');

} // end expandGroup()

//
// Function collapseGroup() is a member function to collapse an expanded group
//
// @param($id object) $id is the jquery id of the group header of the group to collapse
//
// @param(focus boolean) focus is true if the group header has focus, false otherwise
//
// @return N/A
//
treeview.prototype.collapseGroup = function($id, focus) {

  var $group = $id.children('ul');

  // collapse the group
  $group.hide();

  $id.attr('aria-expanded', 'false');

  if (focus == true) {
    $id.children('img').attr('src', 'images/treeContractedFocus.gif');
  }
  else {
    $id.children('img').attr('src', 'images/treeContracted.gif');
  }

  // refresh the list of visible items
  this.$visibleItems = this.$id.find('li:visible');

} // end collapseGroup()

//
// Function toggleGroup() is a member function to toggle the display state of a group
//
// @param($id object) $id is the jquery id of the group header of the group to toggle
//
// @param(focus boolean) focus is true if the group header has focus, false otherwise
//
// @return N/A
//
treeview.prototype.toggleGroup = function($id, focus) {

  var $group = $id.children('ul');

  if ($id.attr('aria-expanded') == 'true') {
    // collapse the group
    this.collapseGroup($id, focus);
  }
  else {
    // expand the group
    this.expandGroup($id, focus);
  }

} // end toggleGroup()

//
// Function bindHandlers() is a member function to bind event handlers to the listitems
//
// return N/A
//
treeview.prototype.bindHandlers = function() {

  var thisObj = this;

  // bind a dblclick handler to the group headers
  this.$groups.dblclick(function(e) {
    return thisObj.handleDblClick($(this), e);
  });

  // bind a click handler
  this.$listitems.click(function(e) {
    return thisObj.handleClick($(this), e);
  });

  // bind a keydown handler
  this.$listitems.keydown(function(e) {
    return thisObj.handleKeyDown($(this), e);
  });

  // bind a keypress handler
  this.$listitems.keypress(function(e) {
    return thisObj.handleKeyPress($(this), e);
  });

  // bind a focus handler
  this.$listitems.focus(function(e) {
    return thisObj.handleFocus($(this), e);
  });

  // bind a blur handler
  this.$listitems.blur(function(e) {
    return thisObj.handleBlur($(this), e);
  });

} // end bindHandlers()

//
// Function doHighlight() is a member function to remove the highlighting from
// other treeview items and apply it to the passed element
//
// @param ($id object) $id is the jQuery object of the element to highlight
//
// @param (isHeader boolean) isHeader is true if $id points to a group header
//
// @return N/A
//
treeview.prototype.doHighlight = function($id, isHeader) {

  // remove the focus highlighting from the treeview items
  // and remove them from the tab order.
  this.$listitems.removeClass('focus').attr('tabindex', '-1');

  // remove the focus image from group headers
  this.$groups.each(function() {
    // add the focus image
    if ($(this).attr('aria-expanded') == 'true') {
      $(this).children('img').attr('src', 'images/treeExpanded.gif');
    }
    else {
      $(this).children('img').attr('src', 'images/treeContracted.gif');
    }
  });

  if (isHeader == true) {
    // add the focus image
    if ($id.attr('aria-expanded') == 'true') {
      $id.children('img').attr('src', 'images/treeExpandedFocus.gif');
    }
    else {
      $id.children('img').attr('src', 'images/treeContractedFocus.gif');
    }
  }


  // apply the focus highlighting and place the element in the tab order
  $id.addClass('focus').attr('tabindex', '0');

} // end doHighlight()

//
// Function handleKeyDown() is a member function to process keydown events for the treeview items
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns false if consuming event; true if not
//
treeview.prototype.handleKeyDown = function($id, e) {

  var curNdx = this.$visibleItems.index($id);
  var isHeader = false;

  // determine if this is a group header
  if (this.$groups.index($prev) != -1) {
    isHeader = true;
  }

  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  switch (e.keyCode) {
    case this.keys.home: {
      this.$groups.first().focus();

      e.stopPropagation();
      return false;
    }
    case this.keys.end: {
      this.$visibleItems.last().focus();

      e.stopPropagation();
      return false;
    }
    case this.keys.enter: {

      if (isHeader == false) {
        // do nothing
        return true;
      }

      this.toggleGroup($id, true);

      e.stopPropagation();
      return false;
    }
    case this.keys.left: {
      
      if (isHeader == false) {
        // do nothing
        return true;
      }

      if ($id.attr('aria-expanded') == 'true') {
        this.collapseGroup($id, true);
      }
      else {
        // move to previous group header
        var prevNdx = this.$groups.index($id) - 1;

        if (prevNdx >= 0) {
          var $prev = this.$groups.eq(prevNdx);
          var parentFound = false;

          while (parentFound == false) {
            if ($prev.find('#' + $id.attr('id')).length > 0) {
              parentFound = true;
              $prev.focus();
              break;
            }
            else {
              // decrement prevNdx to reference the previous
              // group header in the $groups array
              prevNdx--;

              $prev = this.$groups.eq(prevNdx);

              if (prevNdx < 0) {
                // no parent group header
                break;
              }
            }

          } // end while
        }
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.right: {
      
      if (isHeader == false) {
        // do nothing
        return true;
      }

      if ($id.attr('aria-expanded') == 'false') {
        this.expandGroup($id, true);
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.up: {

      if (curNdx > 0) {
        var $prev = this.$visibleItems.eq(curNdx - 1);

        $prev.focus();
      }

      e.stopPropagation();
      return false;
    }
    case this.keys.down: {

      if (curNdx < this.$visibleItems.length - 1) {
        var $next = this.$visibleItems.eq(curNdx + 1);

        $next.focus();
      }
      e.stopPropagation();
      return false;
    }
    case this.keys.asterisk: {
      // expand all groups

      var thisObj = this;

      this.$groups.each(function() {
        thisObj.expandGroup($(this), false);
      });

      e.stopPropagation();
      return false;
    }
  }

  return true;

} // end handleKeyDown

//
// Function handleKeyPress() is a member function to process keypress events for the treeview items
// This function is needed for browsers, such as Opera, that perform window manipulation on kepress events
// rather than keydown. The function simply consumes the event.
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns false if consuming event; true if not
//
treeview.prototype.handleKeyPress = function($id, e) {

  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  switch (e.keyCode) {
    case this.keys.enter:
    case this.keys.home:
    case this.keys.end:
    case this.keys.left:
    case this.keys.right:
    case this.keys.up:
    case this.keys.down: {
      e.stopPropagation();
      return false;
    }
  }

  return true;

} // end handleKeyPress

//
// Function handleDblClick() is a member function to process double-click events for group headers.
// Double-click expands or collapses a group.
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns false if consuming event; true if not
//
treeview.prototype.handleDblClick = function($id, e) {

  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  // apply the focus highlighting
  this.doHighlight($id, true);

  // expand or collapse the group
  this.toggleGroup($id, true);

  e.stopPropagation();
  return false;

} // end handleDblClick

//
// Function handleClick() is a member function to process click events.
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns false if consuming event; true if not
//
treeview.prototype.handleClick = function($id, e) {

  if (e.altKey || e.ctrlKey || e.shiftKey) {
    // do nothing
    return true;
  }

  if (this.$groups.index($id) == -1) {
    // this is a list item

    // apply the focus highlighting
    this.doHighlight($id, false);
  }
  else {
    // this is a group header

    // apply the focus highlighting
    this.doHighlight($id, true);
  }

  e.stopPropagation();
  return false;

} // end handleClick

//
// Function handleFocus() is a member function to process focus events.
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns true
//
treeview.prototype.handleFocus = function($id, e) {

  // only process the event if the focusHandled flag is false
  if (g_focusHandled == false) {

    // prevent encapsulating group headers from responding to
    // the focus event.
    g_focusHandled = true;
  
    if (this.$groups.index($id) == -1) {
      this.doHighlight($id, false);
    }
    else {
      // this is a group header
      this.doHighlight($id, true);
    }

    window.setTimeout(resetFocusFlag, 10);
  }

  return true;

} // end handleFocus

//
// Function handleBlur() is a member function to process blur events.
//
// @param ($id object) $id is the jQuery id of the group header firing event
//
// @param (e object) e is the associated event object
//
// @return (boolean) returns true
//
treeview.prototype.handleBlur = function($id, e) {

  if (this.$groups.index($id) != -1) {
    // this is a group header

    // remove the focus image
    if ($id.attr('aria-expanded') == 'true') {
      $id.children('img').attr('src', 'images/treeExpanded.gif');
    }
    else {
      $id.children('img').attr('src', 'images/treeContracted.gif');
    }
  }

  // remove the focus highlighting
  $id.removeClass('focus');

  return true;

} // end handleBlur 
