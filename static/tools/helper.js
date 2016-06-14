function timeByOffset(origin,offset){
    // origin: "03-14 17:17:14"
    // offset: seconds
    var zp = function (val){
        return (val <= 9 ? '0' + val : '' + val);
    }

    //zero-pad up to two zeroes if needed
    var zp2 = function(val){
        return val <= 99? (val <=9? '00' + val : '0' + val) : ('' + val ) ;
    }

    var date = new Date();
    date.setMonth(parseInt(origin.substring(0,2)));
    date.setDate(parseInt(origin.substring(3,6)));
    date.setHours(parseInt(origin.substring(6,8)));
    date.setMinutes(parseInt(origin.substring(9,11)));
    if (origin.length > 11) {
        date.setSeconds(parseInt(origin.substring(12,14)));
    } else {
        date.setSeconds(0);
    }

    date.setSeconds(date.getSeconds()+offset);

    d = date.getDate();
    m = date.getMonth();
    y = date.getFullYear();
    h = date.getHours();
    min = date.getMinutes();
    s = date.getSeconds();
    return zp(m) + '-' + zp(d) + ' ' + zp(h) + ':' + zp(min) + ':' + zp(s);
}

String.prototype.Trim = function(){
    return this.replace(/(^\s*)|(\s*$)/g, "");
}
String.format = function () {
    if (arguments.length == 0) {
        return null;
    }
    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}

matchColors = [
    ["#F0F0F0","#0000CC","英足总杯"],
    ["#F0F0F0","#0000DB","亚冠杯"],
    ["#F0F0F0","#006633","西甲"],
    ["#F0F0F0","#006699","俄超"],
    ["#F0F0F0","#008888","葡超"],
    ["#F0F0F0","#0088FF","意甲"],
    ["#F0F0F0","#009900","日职联"],
    ["#F0F0F0","#00CCCC","阿甲秋"],
    ["#F0F0F0","#00D200","瑞士甲"],
    ["#F0F0F0","#137AAC","芬超"],
    ["#F0F0F0","#1BA578","瑞士超"],
    ["#F0F0F0","#438E0B","西乙"],
    ["#F0F0F0","#660033","美职业"],
    ["#F0F0F0","#663333","法甲"],
    ["#F0F0F0","#66CCFF","意乙"],
    ["#F0F0F0","#6969E0","丹麦超"],
    ["#F0F0F0","#990099","德甲"],
    ["#F0F0F0","#993333","哥伦甲秋"],
    ["#F0F0F0","#B1A7A7","法乙"],
    ["#F0F0F0","#CA00CA","德乙"],
    ["#F0F0F0","#CC3300","英冠"],
    ["#F0F0F0","#CC3300","英冠附"],
    ["#F0F0F0","#DDDD00","巴西甲"],
    ["#F0F0F0","#F75000","欧冠杯"],
    ["#F0F0F0","#F75000","欧罗巴杯"],
    ["#F0F0F0","#F75000","欧洲杯"],
    ["#F0F0F0","#FF3333","英超"],
    ["#F0F0F0","#FF7000","澳洲甲"],
    ["#F0F0F0","#FF850B","英甲"],
    ["#FFFDF3","#004488","瑞典超"],
    ["#FFFDF3","#006633","西甲"],
    ["#FFFDF3","#006699","俄超"],
    ["#FFFDF3","#0066FF","中超"],
    ["#FFFDF3","#008888","葡超"],
    ["#FFFDF3","#0088FF","意甲"],
    ["#FFFDF3","#009900","日职乙"],
    ["#FFFDF3","#009900","日职联"],
    ["#FFFDF3","#00CCCC","阿甲秋"],
    ["#FFFDF3","#00D200","瑞士甲"],
    ["#FFFDF3","#1BA578","瑞士超"],
    ["#FFFDF3","#438E0B","西乙"],
    ["#FFFDF3","#663333","法甲"],
    ["#FFFDF3","#66CCFF","意乙"],
    ["#FFFDF3","#990099","德甲"],
    ["#FFFDF3","#993333","哥伦甲秋"],
    ["#FFFDF3","#996600","土超"],
    ["#FFFDF3","#CA00CA","德乙"],
    ["#FFFDF3","#CA00CA","德乙附"],
    ["#FFFDF3","#CC3300","英冠"],
    ["#FFFDF3","#FF3333","英超"],
    ["#FFFDF3","#FF6699","荷甲"],
    ["#FFFDF3","#FF7000","世界杯"],
    ["#FFFDF3","#FF7000","澳洲甲"],
    ["#FFFDF3","#FF850B","英甲"],
];

careMatches = [];
careColors = [];

for (var i = 0;i < matchColors.length;i++){
    careMatches.push(matchColors[i][2]);
    m = [];
    m.push(matchColors[i][0]);
    m.push(matchColors[i][1]);
    careColors.push(m);
}
