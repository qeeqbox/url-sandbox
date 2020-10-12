function check_task(task) {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": csrf_token
        }
    });
    $.ajax({
        timeout: (10 * 1000),
        type: "POST",
        url: "/task",
        data: JSON.stringify({
            "task": task
        }),
        contentType: "application/json; charset=utf-8",
        success: function(_task) {
            if (_task === "") {
                setTimeout(function() {
                    check_task(task);
                }, 1000)
            } else {
                 $(".task-details").html(_task);
                 $(".waiting").toggle();
                 //$('.task-details tbody').each(function(){ $(this).toggle()});
            }
        },
    });
}