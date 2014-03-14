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
    date.setSeconds(parseInt(origin.substring(12,14)));

    date.setSeconds(date.getSeconds()+offset);

    d = date.getDate();
    m = date.getMonth();
    y = date.getFullYear();
    h = date.getHours();
    min = date.getMinutes();
    s = date.getSeconds();
    return zp(m) + '-' + zp(d) + ' ' + zp(h) + ':' + zp(min) + ':' + zp(s);
}
