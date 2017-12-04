function citys(){
        $.ajax({
            type:'get',
            url:"{% url 'district' 0 %}",
            dataType:'json',
            async: false,
            success:function(res){
                list = res.data;
                //遍历响应的城市信息
                for(var i=0;i<list.length;i++){
                    $("#cid").append("<option value='"+list[i].id+"'>"+list[i].name+"</option>");
                }
            },
        });

        //获取最后一个下拉框并添加选中事件
        $("select").live('change',function(){
            //获取选中的id号
            var id = $(this).val();
            $(this).nextAll().remove();
            $.ajax({
                url: "/district/"+id,
                type: 'get',
                data: {},
                dataType:'json',
                success:function(res){
                    if(res.data.length<1)
                        return;
                    var data = res.data;
                    var select = $("<select></select>")
                    for(var i=0;i<data.length;i++){
                        $('<option value="'+data[i].id+'">'+data[i].name+'</option>').appendTo(select)
                        //$('select:last').append('<option value="'+data[i].id+'">'+data[i].name+'</option>'); 
                    }
                    $("select:last").after(select);
                }
            });
        });

    }
