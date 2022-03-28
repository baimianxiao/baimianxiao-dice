--[[
不同时间段不同回复模板
by baigugu
version：v1.0.2
介绍：（写的比较粗糙，勿喷）
用的lua的os库，使用需要一定耐心看例子，核心函数不用管，直接看自定义部分，复制例子部分改相关文本或者参数就行，建议使用vscode之类的软件辅助修改
]]--

--初始化回复列表
msg_order={}


--核心函数，不用你改
function time_reply_main(reply_list)
    local hour=tonumber (os.date('%H'))
    for i, v in ipairs(time_config) do
        if (v[1]<= hour and v[2]>= hour) then
            if reply_list[i]==nil then
                return ""
            end
            return table_draw(reply_list[i])
        end
    end
end

function table_draw(tab)
    return tab[ranint(1,#tab)]
end

--自定义部分

--设置时间段，对应着回复列表
time_config={
    {0,4},
    {5,8},
    {9,10},
    {11,13},
    {14,18},
    {19,23}
}

--例子：早上好
function good_morning(msg)--函数名good_morning
    return time_reply_main(list_morning)--time_reply_main(回复列表名)
end

--回复列表对应全局设置的时间
list_morning={
    {
        '凌晨呢'
    },
    {
       "早安，{self}又要开始新研究了……你准备好了吗？",
        "哦哈哟……检测记忆库无缺失……{self}很庆幸没有忘记您……",
        "早上好……准备好面对新的一天了吗？",
        "早安，又是全新的一天……{self}会记录下每一个人的……{self}不愿在失去记忆……",
        "早安……",
        "早上好……",
        "哦哈哟……",
        "早上好，{self}还要继续昨天的研究……",
        '早上好，建议来一杯热牛奶然后再开启一天的活动'
    },
 
    {
        '早安',
        '早上好哦'
    },
    {
       '并不算早了，您还有一天的工作',
       '您昨天是熬夜了么，请注意休息',
        '午好,白面鸮认为该时间段不属于早上',
        '中午好，您可能睡过头了'
    },
    {--可以空

    },
    {

    }
}
--例子结束
--自定义部分结束

--将关键词绑定到函数
msg_order["早上好呀"]="good_morning"
msg_order["早上好"]="good_morning"
msg_order['哦哈哟']='good_morning'