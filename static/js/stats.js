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

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}

function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
    .toString(16)
    .substring(1);
}

function typesort(a, b){
    return a.split('-')[2] > b.split('-')[2];
}



var url = "https://statistik.ub.uni-heidelberg.de/oa_statistik/doc_id/period/?doc_id="+ ids+','+b_id+"&uid="+guid();
console.info(url);
$.getJSON( url, function( data ) {
  var totals = 0;
  for (var i = 0; i < ids.length; i++) {
    var id =  '#'+ids[i].replace(':','_');
    var val = setValue(ids[i]);
    $(id).text(val);
    totals += val;

  }
  $("#total-chapter-files").text(totals);

  // book

  function setValue(elem) {
    try {
      total = data.items[elem].sum.requests;
      }
      catch (e) {
      console.log(b_id[elem],'does not have any values');
      }
      return total;
    };


   normalized_b_id =  b_id[0].replace(':','_');
  $("#"+normalized_b_id).text(setValue(b_id[0]));

  }).fail(function() {
      $('#statistik-button').hide();
      console.log("statistik service unavaliable");
  });
  
