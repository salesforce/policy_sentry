
function add_action(action_name) {
    console.log("in add action");

    let dropdown_values;
    if (action_name == "action") {
        dropdown_values = ["read", "write", "list", "tagging", "permissions-management"]
    } else {
        dropdown_values = ["single-actions", "service-read", "service-write", "service-list", "service-tagging", "service-permissions-management"]
    }
    const tab_var = action_name;
    selected_action = document.getElementById(tab_var+'_name').value;
    arn_name = document.getElementById(tab_var+'_arn').value;
    table = document.getElementById(tab_var+'_table');
    var rowlen = table.rows.length;
    var row = table.insertRow(rowlen);
    row.id = tab_var+"_"+rowlen;
    var n_action = row.insertCell(0);
    var n_arn = row.insertCell(1);
    var n_btn = row.insertCell(2);
    select_tag = document.createElement('select');
    select_tag.setAttribute('name',tab_var+'_name_'+rowlen)
    select_tag.className = 'form-control';
    n_arn.innerHTML = '<input type="text" class="form-control" name="'+tab_var+'_arn_'+ rowlen+'" placeholder="arns seperated by comma" value="'+arn_name+'">';
    n_btn.innerHTML = '<button id="btn'+ rowlen+'" class="btn btn-outline-danger btn-sm" onclick="remove_row(\''+tab_var+'\','+rowlen +')">Delete</button>';
    for(var i =0;i<dropdown_values.length; i++){
        var act = document.createElement("option");
        var actText = document.createTextNode(dropdown_values[i]);
        if(dropdown_values[i] == selected_action){
            act.selected=true;
        }
        act.appendChild(actText);
        select_tag.appendChild(act);
    }
    n_action.appendChild(select_tag);
    n_action.className = 'dropdown_width';
    n_arn.className = 'text_width';
    n_btn.className = 'btn_width'
    document.getElementById(tab_var+'_arn').value="";
    document.getElementById(tab_var+'_set_default').selected=true;
}

function remove_row(table_name, row_index) {
    document.getElementById(table_name+'_'+row_index).remove();
}

function call_api() {
    var data = $( "form" ).serialize();
    $.ajax({
        type: "POST",
        url: '/call_policy',
        data: data,
        success: function(response){
            document.getElementById('final_json').value = JSON.stringify(response, null, 4);
            console.log(JSON.stringify(response));
        }
    });
}
