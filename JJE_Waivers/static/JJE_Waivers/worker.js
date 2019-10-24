
var base_positions = [
    "LW",
    "RW",
    "C",
    "D",
    "G",
    "Util",
    "IR",
    "NA"
];

$('#claim_form').submit(function () {
    enable_everything()
});


function enable_everything() {
    var position = null;
    var pos = null;
    var i = 0;
    for (i = 0; i < base_positions.length; i++) {
        position = base_positions[i];
        pos = $("#" + "add" + position);
        pos.attr("disabled", false);
    }
}


function timer_function() {
    var counterList = $(".timecounter");

    $(counterList).each(function () {
            var ET = $(this).attr('end-time');
            var tm = moment.utc(ET).countdown();
            if (tm.value <= 0) {
                var hr = tm.hours;
                var mn = tm.minutes;
                var sc = tm.seconds;

                var outvm = "";
                if (hr > 0) {
                    if (hr > 10) {
                        outvm += hr;
                        outvm += ":"
                    }
                    else if ((hr < 10) && (hr > 0)) {
                        outvm += ("0" + hr);
                        outvm += ":"
                    }
                }

                if (mn < 10) {outvm += "0"}
                outvm += mn + ":";
                if (sc < 10) {outvm += "0"}
                outvm += sc;
                $(this).text(outvm)
            }
            else {
                var claim_cont = $(this).closest(".claim-container");
                var claim_id = $(claim_cont).attr('id');
                var claim_hr = $(".hr_claim_" + claim_id);

                claim_cont.remove();
                claim_hr.remove();
            }
    });
}

$(document).ready(function () {
    //Start timer
    window.setInterval(timer_function, 1000);
});
