$("#faculty_login_button").click(
        callfaculty_login_function();
        );

var callfaculty_login_function()
{

    $.ajax({
        url:'http:127.0.0.1:8080/faculty/login',
        method:'post',
        data: $('form[name=loginForm]').serialize(),
        dataType: 'json',
        success:function(){
            alert("Login Successful");
            },
        error:function(){
            alert("Login failed");
        },
    });
}
