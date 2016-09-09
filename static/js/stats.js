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

function typesort(a, b){
    return a.split('-')[2] > b.split('-')[2];
}


var script = 'oastats-json.cgi';
var url = "../../../cgi-bin/" + script + "?repo=omphp&type=json&ids=" + ids;
$.getJSON( url, function( data ) {
  var totals = {};
  $.each(data, function (key, value) {
  totals[key] = value.all_years.reduce(function (prev, elem) { return prev + parseInt(elem.volltext); }, 0);
  });
  var statsTableChapters = document.getElementById('statsTableChapters');
  var a_k, full_files;
  var total = {};
  for (let k in totals){
$("#" + k).text(totals[k]);
  a_k = k.split("-");
  if (a_k.length === 3) {

if (total[a_k[2]] !== undefined){
total[a_k[2]] = total[a_k[2]] + totals[k];
}
else {
total[a_k[2]] = totals[k];
}
}
}


full_files = $(".full_file");
  $.each(full_files, function(index, value) {
  for (var prop in total) {
  if (value.id.indexOf(prop) > 0) {
  console.log(total[prop]);
    total[prop] = total[prop] - value.innerText;
  }
  }
  });
  for (var prop in total) {
var s = $("#total-chapter-" + prop);
  s.text(total[prop]);
}
  }).fail(function() {
      $('#statistik-button').hide();
      console.log("statistik service unavaliable");
  });
  
