$(function () {

  /* Functions */

  let loadForm = function () {
    let btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-task").modal("show");
      },
      success: function (data) {
        $("#modal-task .modal-content").html(data.html_form);
      }
    });
  };

  let saveForm = function () {
    let form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#task-list").html(data.html_task_list);
          $("#modal-task").modal("hide");
        }
        else {
          $("#modal-task .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  let doneTask = function () {
    let btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      success: function (data) {
        $("#task-list").html(data.html_task_list);
      }
    });
  };

  /* Binding */

  // Create task
  $(".js-create-task").click(loadForm);
  $("#modal-task").on("submit", ".js-task-create-form", saveForm);

  // Update task
  $("#task-list").on("click", ".js-update-task", loadForm);
  $("#modal-task").on("submit", ".js-task-update-form", saveForm);

  // Delete task
  $("#task-list").on("click", ".js-delete-task", loadForm);
  $("#modal-task").on("submit", ".js-task-delete-form", saveForm);

  // Completed task
  $("#task-list").on("click", ".js-completed-task", doneTask);

});