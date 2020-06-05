
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
