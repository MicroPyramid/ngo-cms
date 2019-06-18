// JavaScript Document
$(document).ready(function (e) {
  //to of na bar
  $("#wide-ver-bar").click(function (e) {
    e.stopPropagation();
    $("#ver-bar-i").css("display", "none");
    $("#ver-bar-sm-i").css("display", "block");
    $(this).css("display", "none");
    $("#small-ver-bar").css("display", "block");
	$(".container").css("margin-left","155px");
  });
  $("#small-ver-bar").click(function (e) {
    e.stopPropagation();
    $("#ver-bar-sm-i").css("display", "none");
    $("#ver-bar-i").css("display", "block");
    $(this).css("display", "none");
    $("#wide-ver-bar").css("display", "block");
	$(".container").css("margin-left","255px");
  });
  return false;
  //tog of nav bar
});


//login
$(document).ready(function() {
  $("#form_login").submit(function(e) {
    e.preventDefault();
    $.post("/admin/", $("#form_login").serialize(), function(data) {
      if (data.error == false) {
        window.location = "/admin/";
      } else {
        $("#message").html(data.message);
      }
    }, "json");
  });
});

    var quill = new Quill('#editor-container', {
      modules: {
        toolbar: [
          [{ header: [1, 2, false] }],
          ['bold', 'italic', 'underline'],
          ['image', 'code-block']
        ]
      },
      theme: 'snow' // or 'bubble'
    });

    var preciousContent = document.getElementById('myPrecious');
    var justTextContent = document.getElementById('justText');
    var justHtmlContent = document.getElementById('justHtml');

    quill.on('text-change', function() {
      var delta = quill.getContents();
      var text = quill.getText();
      var justHtml = quill.root.innerHTML;
      $('#description').val(justHtml);
    });

$(document).ready(function() {
  $('#banner_add_form').ajaxForm({
    dataType: 'json',
    data: $('#banner_add_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/banner/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        // alert(data)
        console.log(data)
        $.each(data, function(key, value) {
          $('#' + key).text(value);
          $('.error').css('color', 'red');
        });
      }
    }
  });
});
$('#banner_add_save').click(function(e) {
  e.preventDefault();
  $('#banner_add_form').submit();
});
$("#banner_add_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/banner/list/");
});

$('#banner_add_title1').keyup(function() {
  var name_val=$("#banner_add_title1").val().toLowerCase();
  $('#banner_add_title1').val(name_val)
});


//banner-edit

$(document).ready(function() {
  $('#banner_edit_form').ajaxForm({
    dataType: 'json',
    data: $('#banner_edit_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/banner/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
        });
      }
    }
  });
});
$('#banner_edit_save').click(function(e) {
  e.preventDefault();
  $('#banner_edit_form').submit();
});
$("#banner_edit_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/banner/list/");
});
$('#banner_edit_title1').keyup(function() {
  var name_val=$("#banner_edit_title1").val().toLowerCase();
  $('#banner_edit_title1').val(name_val)
});


//banner-list

$('.remove_banner').click(function(e) {
var result = confirm("Are You Sure You Want to delete?");
if (result === false) {
  e.preventDefault();
}
});

//category-add

$(document).ready(function() {
  $('#category_add_form').ajaxForm({
    dataType: 'json',
    data: $('#category_add_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/category/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
          $('.error').css('color', 'red');
        });
      }
    }
  });
});
$('#category_add_save').click(function(e) {
  e.preventDefault();
  $('#category_add_form').submit();
});
$("#category_add_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/category/list/");
});
$().ready(function() {
  $('.category_add_slug1').slugify('#category_add_name1');
  var pigLatin = function(str) {
    return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
  }
  $('#pig_latin').slugify('#category_add_name1', {
    slugFunc: function(str, originalFunc) {
      return pigLatin(originalFunc(str));
    }
  });
});
$('#category_add_name1').keyup(function() {
  $('#category_add_slug1').val($("#category_add_name1").val())
});

//category-edit

$(document).ready(function() {
  $('#category_edit_form').ajaxForm({
    dataType: 'json',
    data: $('#category_edit_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/category/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
          $('.error').css('color', 'red');
        });
      }
    }
  });
});
$('#category_edit_save').click(function(e) {
  e.preventDefault();
  $('#category_edit_form').submit();
});
$("#category_edit_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/category/list/");
});

$().ready(function() {
  $('.category_edit_slug1').slugify('#category_edit_name1');
  var pigLatin = function(str) {
  return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
  }
  $('#pig_latin').slugify('#category_edit_name1', {
    slugFunc: function(str, originalFunc) {
      return pigLatin(originalFunc(str));
    }
  });
});

$('#category_edit_name1').keyup(function() {
  var name_val=$("#category_edit_name1").val().toLowerCase();
  $('#category_edit_slug1').val(name_val)
});


//category-list

$('.remove_category').click(function(e) {
  var result = confirm("Are You Sure You Want to delete?");
  if (result === false) {
    e.preventDefault();
  }
});



//Change-Password

$(document).ready(function() {
  $('#change_pwd_form').ajaxForm({
    dataType: 'json',
    data: $('#change_pwd_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/change_password/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
        });
      }
    }
  });
});
$('#change_pwd_save').click(function(e) {
  e.preventDefault();
  $('#change_pwd_form').submit();
});


//menu_add
$(document).ready(function() {
  $('#menu_add_form').ajaxForm({
    dataType: 'json',
    data: $('#menu_add_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/menu/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
          $('.error').css('color', 'red');
        });
      }
    }
  });
});
$('#menu_add_save').click(function(e) {
  e.preventDefault();
  $('#menu_add_form').submit();
});
$("#menu_add_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/menu/list/");
});
$('#menu_add_name1').keyup(function() {
  var name_val=$("#menu_add_name1").val().toLowerCase();
  $('#menu_add_slug1').val(name_val)
});

//menu-edit

$(document).ready(function() {
  $('#menu_edit_form').ajaxForm({
    dataType: 'json',
    data: $('#menu_edit_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/menu/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value);
          $('.error').css('color', 'red');
        });
      }
    }
  });
});
$('#menu_edit_save').click(function(e) {
  e.preventDefault();
  $('#menu_edit_form').submit();
});
$("#menu_edit_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/menu/list/");
});

$('#menu_edit_name1').keyup(function() {
  var name_val=$("#menu_edit_name1").val().toLowerCase();
  $('#menu_edit_slug1').val(name_val)
});

//menu-list

$('.sub-menu').css("display", "none");
$('.sub-sub-menu').css("display", "none");
$(".tog-d").click(function(e) {
  $(this).hide();
  $(this).next().show();
  clicked = $(this).parent().parent().attr('class');
  clicked_tr = $(this).parent().parent()
  if (clicked == 'main-menu') {
    var sibling = $(clicked_tr).next();
    while (true) {
      console.log($(sibling).attr('class'))
      if ($(sibling).attr('class') == 'main-menu') {
        break;
      }
      if (!$(sibling).attr('class')) {
        break;
      }
      if ($(sibling).attr('class') == 'sub-menu') {
        $(sibling).show();
      }
      sibling = $(sibling).next();
    }
  } else if (clicked == 'sub-menu') {
    var sibling = $(clicked_tr).next();
    while (true) {
      if ($(sibling).attr('class') != 'sub-sub-menu') {
        break;
      }
      $(sibling).show();
      sibling = $(sibling).next();
    }
  } else {}
  return false;
});
$(".tog-u").click(function(e) {
  $(this).hide();
  $(this).prev().show();
  clicked = $(this).parent().parent().attr('class');
  clicked_tr = $(this).parent().parent()
  if (clicked == 'main-menu') {
    var sibling = $(clicked_tr).next();
    while (true) {
      if ($(sibling).attr('class') == 'main-menu') {
        break;
      }
      if (!$(sibling).attr('class')) {
        break;
      }
      $(sibling).hide();
      $(sibling).children().first().children('.tog-u').hide();
      $(sibling).children().first().children('.tog-u').prev().show();
      sibling = $(sibling).next();
    }
  } else if (clicked == 'sub-menu') {
    var sibling = $(clicked_tr).next();
    while (true) {
      if ($(sibling).attr('class') != 'sub-sub-menu') {
        break;
      }
      $(sibling).hide();
      sibling = $(sibling).next();
    }
  } else {}
  return false;
});

$('.remove_menu').click(function(e) {
  var result = confirm("Are You Sure You Want to delete?");
  if (result == false) {
    e.preventDefault();
  }
});



//event-list
$('.remove_event').click(function(e) {
  var result = confirm("Are You Sure You Want to delete?");
  if (result === false) {
    e.preventDefault();
  }
});

//page_list

$('.remove_page').click(function(e) {
  var result = confirm("Are You Sure You Want to delete?");
  if (result === false) {
    e.preventDefault();
  }
});



//post_list

$('.remove_article').click(function(e) {
  var result = confirm("Are You Sure You Want to delete?");
  if (result === false) {
    e.preventDefault();
  }
});


//event-add

$(document).ready(function() {
  $("#event_add_datepicker_start").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-55:c',
    dateFormat: "yy-mm-dd"
  });
  $("#event_add_datepicker_end").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-55:c',
    dateFormat: "yy-mm-dd"
  });
  $('#event_add_form').ajaxForm({
    dataType: 'json',
    data: $('#event_add_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/event/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value)
          $('.error').css('color', 'red')
        });
      }
    }
  });
});
$('#event_add_save').click(function(e) {
  e.preventDefault();
  $('#event_add_form').submit();
});
$("#event_add_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/event/list/");
});


$().ready(function() {
  $('.event_add_slug1').slugify('#event_add_name1');
  var pigLatin = function(str) {
    return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
  }
  $('#pig_latin').slugify('#event_add_name1', {
    slugFunc: function(str, originalFunc) {
      return pigLatin(originalFunc(str));
    }
  });
});



//event_edit


$(document).ready(function() {
  $("#event_edit_datepicker_start").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-55:c',
    dateFormat: "yy-mm-dd"
  });
  $("#event_edit_datepicker_end").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: 'c-55:c',
    dateFormat: "yy-mm-dd"
  });
  $('#event_edit_form').ajaxForm({
    dataType: 'json',
    data: $('#event_edit_form').serialize(),
    type: "POST",
    success: function(data) {
      if (data.error == false) {
        alert(data.data);
        window.location = '/admin/event/list/';
      } else {
        $('.error').text('');
        $('.error').show();
        $.each(data, function(key, value) {
          $('#' + key).text(value)
          $('.error').css('color', 'red')
        });
      }
    }
  });
});
$('#event_edit_save').click(function(e) {
  e.preventDefault();
  $('#event_edit_form').submit();
});
$("#event_edit_cancel").click(function(e) {
  e.preventDefault();
  window.location.replace("/admin/event/list/");
});

$().ready(function() {
  $('.event_edit_slug1').slugify('#event_edit_name1');
  var pigLatin = function(str) {
    return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
  }
  $('#pig_latin').slugify('#event_edit_name1', {
    slugFunc: function(str, originalFunc) {
      return pigLatin(originalFunc(str));
    }
  });
});
$('#event_edit_name1').keyup(function() {
  var name_val=$("#event_edit_name1").val().toLowerCase();
  $('#event_edit_slug1').val(name_val)
});


//page-add

  var max_fields = 45; //maximum input boxes allowed
  var wrapper = $(".input_fields_wrap"); //Fields wrapper
  var add_button = $(".page_add_field_button"); //Add button ID
  var x = 1; //initlal text box count
  $(add_button).click(function(e) { //on add input button click
    console.log('add ')
    e.preventDefault();
    if (x < max_fields) { //max input box allowed
      x++; //text box increment
      $(wrapper).append('<div class="txt-box-div adjust-sc"><input type="file" name="photos"/><a href="#" class="remove_field" style="display:margin-left:159px;">Remove</a></div>'); //add input box
    }
  });
  $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
  });
  $(document).ready(function() {
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');
    $('#page_add_form').ajaxForm({
      dataType: 'json',
      data: $('#page_add_form').serialize(),
      type: "POST",
      beforeSend: function() {
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal);
        percent.html(percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal);
        console.log(percentVal);
        percent.html(percentVal);
      },
      success: function(data) {
        var percentVal = '100%';
        bar.width(percentVal);
        percent.html(percentVal);
        if (data.error == false) {
          alert(data.data);
          window.location = '/admin/page/list/';
        } else {
          $('.error').text('');
          $('.error').show();
          $.each(data, function(key, value) {
            $('#' + key).text(value);
            $('.error').css('color', 'red');
          });
        }
      }
    });
  });
  $('#page_add_save').click(function(e) {
    e.preventDefault();
    $('#page_add_form').submit();
  });
  $("#page_add_cancel").click(function(e) {
    e.preventDefault();
    window.location.replace("/admin/page/list/");
  });
  $().ready(function() {
    $('.page_add_slug1').slugify('#page_add_title1');
    var pigLatin = function(str) {
      return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
    }
    $('#pig_latin').slugify('#page_add_title1', {
      slugFunc: function(str, originalFunc) {
        return pigLatin(originalFunc(str));
      }
    });
  });

//page-edit
  var max_fields = 45; //maximum input boxes allowed
  var wrapper = $(".input_fields_wrap"); //Fields wrapper
  var add_button = $(".edit_field_button"); //Add button ID
  var x = 1; //initlal text box count
  $(add_button).click(function(e) { //on add input button click
    e.preventDefault();
    if (x < max_fields) { //max input box allowed
      x++; //text box increment
      $(wrapper).append('<div class="txt-box-div adjust-sc"><input type="file" name="photos"/><a href="#" class="remove_field" style="display:margin-left:159px;">Remove</a></div>'); //add input box
    }
  });
  $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
  });

  $(document).ready(function() {
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');
    $('#page_edit_form').ajaxForm({
      dataType: 'json',
      data: $('#page_edit_form').serialize(),
      type: "POST",
      beforeSend: function() {
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal);
        percent.html(percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal);
        console.log(percentVal);
        percent.html(percentVal);
      },
      success: function(data) {
        var percentVal = '100%';
        bar.width(percentVal);
        percent.html(percentVal);
        if (data.error == false) {
          alert(data.data);
          window.location = '/admin/page/list/';
        } else {
          $('.error').text('');
          $('.error').show();
          $.each(data, function(key, value) {
            $('#' + key).text(value);
            $('.error').css('color', 'red');
          });
        }
      }
    });
  });
  $('#page_edit_save').click(function(e) {
    e.preventDefault();
    $('#page_edit_form').submit();
  });
  $("#page_edit_cancel").click(function(e) {
    e.preventDefault();
    window.location.replace("/admin/page/list/");
  });

  $().ready(function() {
    $('.page_edit_slug1').slugify('#page_edit_title1');
    var pigLatin = function(str) {
      return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
    }
    $('#pig_latin').slugify('#page_edit_title1', {
      slugFunc: function(str, originalFunc) {
        return pigLatin(originalFunc(str));
      }
    });
  });

  $('#page_edit_title1').keyup(function() {
    var name_val=$("#page_edit_title1").val().toLowerCase();
    $('#page_edit_slug1').val(name_val)
});


//post-add
  var max_fields = 45; //maximum input boxes allowed
  var wrapper = $(".input_fields_wrap"); //Fields wrapper
  var add_button = $(".padd_field_button"); //Add button ID
  var x = 1; //initlal text box count
  $(add_button).click(function(e) { //on add input button click
    e.preventDefault();
    if (x < max_fields) { //max input box allowed
      x++; //text box increment
      $(wrapper).append('<div class="txt-box-div adjust-sc"><input type="file" name="photos"/><a href="#" class="remove_field" style="display:margin-left:159px;">Remove</a></div>'); //add input box
    }
  });
  $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
  });
  $(document).ready(function() {
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');
    $('#post_add_form').ajaxForm({
      dataType: 'json',
      data: $('#post_add_form').serialize(),
      type: "POST",
      beforeSend: function() {
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal);
        percent.html(percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal);
        console.log(percentVal);
        percent.html(percentVal);
      },
      success: function(data) {
        var percentVal = '100%';
        bar.width(percentVal);
        percent.html(percentVal);
        if (data.error == false) {
          alert(data.data);
          window.location = '/admin/article/list/';
        } else {
          $('.error').text('');
          $('.error').show();
          $.each(data, function(key, value) {
            if (key == 'description') {
              $('#id_' + key).text(value)
            } else {
              $('#' + key).text(value);
            }
            $('.error').css('color', 'red')
          });
        }
      }
    });
  });
  $('#post_add_save').click(function(e) {
    e.preventDefault();
    $('#post_add_form').submit();
  });
  $("#post_add_cancel").click(function(e) {
    e.preventDefault();
    window.location.replace("/admin/article/list/");
  });

  $().ready(function() {
    $('.post_add_slug1').slugify('#post_add_title1');
    var pigLatin = function(str) {
      return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
    }
    $('#pig_latin').slugify('#post_add_title1', {
      slugFunc: function(str, originalFunc) {
        return pigLatin(originalFunc(str));
      }
    });
  });

  function onAddTag(tag) {
    alert("Added a tag: " + tag);
  }

  function onRemoveTag(tag) {
    alert("Removed a tag: " + tag);
  }

  function onChangeTag(input, tag) {
    alert("Changed a tag: " + tag);
  }
  $(function() {
    $('#tags_1').tagsInput({
      width: 'auto'
    });
    $('#tags_2').tagsInput({
      width: 'auto',
      onChange: function(elem, elem_tags) {
        var languages = ['php', 'ruby', 'javascript'];
        $('.tag', elem_tags).each(function() {
          if ($(this).text().search(new RegExp('\\b(' + languages.join('|') + ')\\b')) >= 0)
            $(this).css('background-color', 'yellow');
        });
      }
    });
    $('#tags_3').tagsInput({
      width: 'auto',
      //autocomplete_url:'test/fake_plaintext_endpoint.html' //jquery.autocomplete (not jquery ui)
      autocomplete_url: 'test/fake_json_endpoint.html' // jquery ui autocomplete requires a json endpoint
    });
    // Uncomment this line to see the callback functions in action
    //      $('input.tags').tagsInput({onAddTag:onAddTag,onRemoveTag:onRemoveTag,onChange: onChangeTag});
    // Uncomment this line to see an input with no interface for adding new tags.
    //      $('input.tags').tagsInput({interactive:false});
  });

//post-edit

  var max_fields = 45; //maximum input boxes allowed
  var wrapper = $(".input_fields_wrap"); //Fields wrapper
  var add_button = $(".pedit_field_button"); //Add button ID
  var x = 1; //initlal text box count
  $(add_button).click(function(e) { //on add input button click
    e.preventDefault();
    if (x < max_fields) { //max input box allowed
      x++; //text box increment
      $(wrapper).append('<div class="txt-box-div adjust-sc" ><input type="file" name="photos"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
    }
  });
  $(wrapper).on("click", ".remove_field", function(e) { //user click on remove text
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
  });

  $(document).ready(function() {
    var bar = $('.bar');
    var percent = $('.percent');
    var status = $('#status');
    $('#post_edit_form').ajaxForm({
      dataType: 'json',
      data: $('#post_edit_form').serialize(),
      type: "POST",
      beforeSend: function() {
        status.empty();
        var percentVal = '0%';
        bar.width(percentVal);
        percent.html(percentVal);
      },
      uploadProgress: function(event, position, total, percentComplete) {
        var percentVal = percentComplete + '%';
        bar.width(percentVal);
        console.log(percentVal);
        percent.html(percentVal);
      },
      success: function(data) {
        var percentVal = '100%';
        bar.width(percentVal);
        percent.html(percentVal);
        if (data.error == false) {
          alert(data.data);
          window.location = '/admin/article/list';
        } else {
          $('.error').text('');
          $('.error').show();
          $.each(data, function(key, value) {
            if (key == 'description') {
              $('#id_' + key).text(value)
            } else {
              $('#' + key).text(value);
            }
            $('.error').css('color', 'red')
          });
        }
      }
    });
  });
  $('#post_edit_save').click(function(e) {
    e.preventDefault();
    $('#post_edit_form').submit();
  });
  $("#post_edit_cancel").click(function(e) {
    e.preventDefault();
    window.location.replace("/admin/article/list/");
  });

  $().ready(function() {
    $('.post_edit_slug1').slugify('#post_edit_title1');
    var pigLatin = function(str) {
      return str.replace(/(\w*)([aeiou]\w*)/g, "$2$1ay");
    }
    $('#pig_latin').slugify('#post_edit_title1', {
      slugFunc: function(str, originalFunc) {
        return pigLatin(originalFunc(str));
      }
    });
  });

  function onAddTag(tag) {
    alert("Added a tag: " + tag);
  }

  function onRemoveTag(tag) {
    alert("Removed a tag: " + tag);
  }

  function onChangeTag(input, tag) {
    alert("Changed a tag: " + tag);
  }
  $(function() {
    $('#tags_1').tagsInput({
      width: 'auto'
    });
    $('#tags_2').tagsInput({
      width: 'auto',
      onChange: function(elem, elem_tags) {
        var languages = ['php', 'ruby', 'javascript'];
        $('.tag', elem_tags).each(function() {
          if ($(this).text().search(new RegExp('\\b(' + languages.join('|') + ')\\b')) >= 0)
            $(this).css('background-color', 'yellow');
        });
      }
    });
    $('#tags_3').tagsInput({
      width: 'auto',
      autocomplete_url: 'test/fake_json_endpoint.html'
    });
  });

  $('#post_edit_title1').keyup(function() {
    var name_val=$("#post_edit_title1").val().toLowerCase();
    $('#post_edit_slug1').val(name_val)
});

