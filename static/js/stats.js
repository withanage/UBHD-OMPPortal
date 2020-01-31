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

function typesort(a, b) {
    return a.split('-')[2] > b.split('-')[2];
}

/**
 *
 * @param data Response data
 * @param id  input id
 * @returns { value}
 */
function setValue(data, id) {
    try {
        total = data.items[id].sum.requests;
        return total;

    } catch (e) {
        console.info(e, id, 'does not have any values');
    }

};

var url = "https://statistik.ub.uni-heidelberg.de/oa_statistik/doc_id/period/?doc_id=" + chapter_ids + ',' + book_id + "&uid=" + guid();

/**
 *  get data from url and set values
 */
$.getJSON(url, function (data) {

    var chapter_total = 0;

    // set chapter  values

    for (var i = 0; i < chapter_ids.length; i++) {

        var chapter_div = '#' + chapter_ids[i].replace(':', '_');

        var chapter_val = setValue(data, chapter_ids[i]);
        if (parseInt(chapter_val)!==0) {
            $(chapter_div).text(chapter_val);
        }

        chapter_total += chapter_val;

    }

    // set chapter total
    $("#total-chapter-files").text(chapter_total);



    // set book value(s)

    var b = book_id[0].replace(':', '_');

    $("#" + b).text(setValue(data, book_id));

}).fail(function () {

    $('#statistik-button').hide();

    console.error("statistik service unavaliable");
});

