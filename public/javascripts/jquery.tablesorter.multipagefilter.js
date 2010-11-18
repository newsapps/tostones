(function($){
  $.extend({
    tablesorterMultiPageFilter : new function(){

      function replaceRows(table){
        // clear the table body
        $.tablesorter.clearTableBody(table);
        var tableBody = $(table.tBodies[0]);
        
        for(var i = 0; i < table.config.collection.length; i++) {          
          var o = table.config.collection[i];
          var l = o.length;
          for(var j=0; j < l; j++) {
            tableBody[0].appendChild(o[j]);
          }
        }
        $(table).trigger("applyWidgets");
      }
      
      
      function renderTable(table){
        var newString = table.config.filterSelector[0].value;
        if(newString.length > 1){
          if(table.config.container){
            table.config.container.hide();
          }
          
          var toShow = [];
          newString = $.trim(newString);
          var words = newString.toLowerCase().split(" ");          
          
          // no change, don't do anything
          if (newString === table.config.string) return false;
          // press was just a string
          if (newString[-1] === " ") { table.config.string = newString; return false; }
          // most of the string is old
          if (newString.indexOf(table.config.string) > -1){
            // don't change the search array but we only need the last word
            words = [words.pop()];
          } else {
            // we need to search all rows
            table.config.collection = table.config.rowsCopy.slice(0);
          };
          
          // split out words
          len = table.config.collection.length;
          var counter = 0;
          for(var j = 0; j < len; j++ ){
            var text = table.config.collection[j].text().toLowerCase();
            for (var i=0; i < words.length; i++) {
              if (text.indexOf(words[i]) > -1) {
                toShow.push(table.config.collection[j]);
              } 
            }
            counter++;
          };
          table.config.collection = toShow.slice(0);
          replaceRows(table);
          table.config.string     = newString;
        } else {
          table.config.string     = "";
          table.config.collection = table.config.rowsCopy.slice(0);
          if(table.config.container){
            table.config.container.show();
          } else {
            replaceRows(table);
          }
        }
      }
      
      this.defaults = {
        filterSelector: $("#filter")
      }
      
      this.init = function(settings) {
        return this.each(function(){
          config = $.extend(this.config, $.tablesorterMultiPageFilter.defaults, settings);
          
          var table  = this, 
              filter = config.filterSelector
          ;

          // save old appenders and define a new one that grabs the row cache and saves it
          if(!table.config.rowsCopy){
            var oldAppend = config.appender || function (table, rows) {};
            this.config.appender = function(table, rows){
              table.config.rowsCopy = rows;
              oldAppend(table, rows);
            }
            $(this).trigger("appendCache");
          }
          table.config.string = "";
          table.config.collection = [];
          table.config.collection = table.config.rowsCopy.slice(0)
            
          function filterMe(){
            renderTable(table);
            return false;
          }
          setInterval(filterMe, 250);
          $(filter).submit(filterMe);
        });
      }
    }
  });
  
  
  $.fn.extend({
    tablesorterMultiPageFilter: $.tablesorterMultiPageFilter.init
  });
}(jQuery))