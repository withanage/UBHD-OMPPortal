/* 
 
 * Copyright 07-Jan-2016, 12:52:49
 *
 * Author    : Dulip Withanage , University of Heidelberg
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


/** statistics  * */
    $('#statistik-button').click(function(){
     $('#oas').slideToggle()
   });
   var script = 'oastats-json.cgi';
   var url = "../../../cgi-bin/"+script+"?repo=omphp&type=json&ids="+ids;
  var count, chapter_pdf, chapter_xml;
  //initialize
  chapter_pdf = 0;
  chapter_xml = 0;
    
  var full_file_ids = [];
  
  $.getJSON( url, function( data ) {
   $.each(data, function(index,value) {
    count = 0;
    $.each(value.all_years, function(index2,value2) {
          count += parseInt(value2.volltext);
          if (index.indexOf('xml') > -1 ) {
               if (index != full_xml) {
                  chapter_xml+= parseInt(value2.volltext);
                }
           }
           
          if (index.indexOf('pdf') > -1) {
              if (index != full_pdf) {
             chapter_pdf+= parseInt(value2.volltext);
           }
          }
         
        $('#chapter_pdf').text(parseInt(chapter_pdf));
        $('#chapter_xml').text(parseInt(chapter_xml));
      });
      $('#'+index).text(parseInt(count));
       
  });
  }).fail(function() {
      $('#statistik-button').hide();
      console.log("statistik service unavaliable");
  });
  
    
  
 
