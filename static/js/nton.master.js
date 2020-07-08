
// $(function () {
//   flatpickr("#id_signed", {defaultDate: signed,
//                           enableTime: true,
//                           allowInput: true,
//                           dateFormat: "Y-m-d",
//                         });
//   });
// $.ajax({
//   url: $("#container").attr("data-url"),
//   dataType: 'json',
//   success: function (data) {
//     Highcharts.chart("container", data);
//   }
// });
// $.ajax({
//   url: $("#container2").attr("data-url"),
//   dataType: 'json',
//   success: function (data) {
//     Highcharts.chart("container2", data);
//     $(".dateTimeField").val()=
//   }
// });
$(function () {
  try {
    flatpickr(".dateTimeField",
      {defaultDate: $(".dateTimeField").val(),
      enableTime: true,
      allowInput: true,
      time_24hr: true,
      dateFormat: "Y-m-d H:m",
    });
  }

  catch(err) {
        console.log(err);
        return;
      }
});
$(function () {
try {
  flatpickr(".dateField",
    {defaultDate: $(".dateField").val(),
    allowInput: true,
    dateFormat: "Y-m-d",
    });
}

  catch(err) {
      console.log(err);
      return;
}
});
$(function () {
  try {
    if ($("#id_url").val() == '') {
      $("#id_url").val('http://');
    }
  }

  catch(err) {
        console.log(err);
        return;
      }
});

function chartloader(e) {
  div = document.getElementById(e);
  $.ajax({
    url: div.getAttribute('data-url'),
    dataType: 'json',
    success: function (data) {
      var chart = Highcharts.chart(e, data);
      // chart.setSize(null);
    }
  });
};

  $("#id_categorie").change(function () {
    loader = true;
    var url = $("#quesionForm").attr("data-categorie-url");
    var categorieId = $(this).val();
    if (categorieId) {

      $.ajax({
        url: url,
        data: {
          'categorie': categorieId
        },
        success: function (data) {
            $("#souscategorieForm").collapse('show');
            $("#id_souscategorie").html(data);
         }
      });
    }
    else {
      $("#souscategorieForm").collapse('hide');
      $("#categoryGrow").collapse('hide');

    }
  });


  var editor = new MediumEditor('.editable', {
    buttonLabels: 'fontawesome',
        toolbar: {
            buttons: ['bold', 'italic',  'justifyCenter',
                'anchor', 'underline',  'strikethrough',
                'subscript', 'superscript', 'anchor',
                'quote', 'orderedlist', 'unorderedlist',
                'indent', 'outdent', 'justifyLeft', 'justifyCenter',
                'justifyRight', 'justifyFull',
                'h1', 'h2', 'h3',  'h4', 'h5', 'h6',
            ]
        }
    });
