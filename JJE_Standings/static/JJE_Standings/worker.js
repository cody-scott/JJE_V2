var base_url = location["protocol"] + "//" + location["host"] + "/";
var standings_api = base_url + "api" + "/";
var current_standings_url = standings_api + "standings/";
var all_standings_url = standings_api + "all_standings/";

var colors = [
    '#FF6666',
    '#FFB266',
    '#FFFF66',
    '#B2FF66',
    '#66FF66',
    '#66FFB2',
    '#66FFFF',
    '#66B2FF',
    '#6666FF',
    '#B266FF',
    '#FF66FF',
    '#FF66B2'
];
var team_colors = {};

var standings_data;
var all_standings_data;
var week_labels;

function get_standings() {
    $.getJSON(
        current_standings_url + "?format=json", function(data) {
            standings_data = process_data(data);

            for (var i=0; i<data.length; i++) {
                var tm = data[i]['team']['team_name'];
                team_colors[tm] = colors[i];
            }

            create_chart();

            get_all_standings();
        }
    )
}

function get_all_standings() {
    $.getJSON(
        all_standings_url + "?format=json", function(data) {
            all_standings_data = process_all_standings(data);
            create_season_chart();
        }
    )
}

// var dt;
// function set_team_colors() {
//         $.getJSON(
//         current_standings_url + "?format=json", function(data) {
//             dt = data;
//
//             for (var i=0; i<data.length; i++) {
//                 var tm = data[i]['team']['team_name'];
//                 team_colors[tm] = colors[i];
//             }
//
//             load_standings();
//         }
//     )
// }


function load_standings() {

    get_all_standings();
}


function process_data(data) {
    var dt = [];
    var lbl = [];
    for (var i=0; i < data.length; i++) {
        var current_team = data[i];
        lbl.push(current_team['team']['team_name']);
        dt.push(current_team['stat_point_total'])
    }
    var out_data = {
        labels: lbl,
        datasets: [{
            data: dt,
            backgroundColor: colors
        }]
    };
    return out_data;
}

function sortNumber(a,b) {
    return a - b;
}

function sortSeasonNumber(a, b) {
    a = parseInt(a["x"].replace("Week ",""));
    b = parseInt(b["x"].replace("Week ",""));
    return a-b
}

function process_all_standings(data) {
    var out_dct = {};
    var week_list = [];

    for (var i=0; i < data.length; i++) {
        var c_row = data[i];
        var tm = c_row['team']['team_name'];
        var standings_week_int = parseInt(c_row["standings_week"]);
        var standings_points_int = parseInt(c_row["stat_point_total"]);
        if (!out_dct[tm]) {
            out_dct[tm] = [];
        }
        out_dct[tm].push(
            {x: "Week " + standings_week_int, y: standings_points_int}
        );
        if (week_list.indexOf(standings_week_int) < 0) {
            week_list.push(standings_week_int)
        }
        week_list.sort(sortNumber);
    }
    week_labels = week_list.map(function(x) { return ["Week " + x]});
    var values = [];
    var tmp_keys = [];

    //gets a list of the team names
    for (var key in out_dct) {
        tmp_keys.push(key);
    }
    //this sorts the teams to alphabetical
    tmp_keys.sort();

    for (var i=0; i<tmp_keys.length; i++) {
        var key = tmp_keys[i];
        var tmp = {
            label: key,
            data: out_dct[key].sort(sortSeasonNumber),
            fill: false,
            borderColor: team_colors[key],
            backgroundColor: team_colors[key]
        };
        values.push(tmp);
    }

    return values;
}

var myChart;
function create_chart() {
    var ctx = document.getElementById("current_standings_chart");

    myChart = new Chart(ctx, {
        type: 'bar',
        data: standings_data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    maxBarThickness: 50,
                    ticks: {
                        autoSkip: false
                    }
                }],
            },
            legend: {
                display: false
            },
        }
    });
}

function create_season_chart() {
    var ctx = document.getElementById("season_chart");

    var season_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: week_labels,
            datasets: all_standings_data
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }],
                xAxes: [],
            },
            legend: {
                display: true
            },
            animation: {
                duration: 0, // general animation time
            },
            hover: {
              animationDuration: 0, // duration of animations when hovering an item
            },
        }
    });
}



function check_chart_hidden() {
    var hidden = $(".canvas_column").attr('hidden');
    if (hidden === 'hidden') {
        return false;
    }
    else {
        return true;
    }
}

function hide_chart() {
    $(".land_view").attr('hidden', '');
    $(".port_view").removeAttr('hidden');
}

function show_chart() {
    $(".land_view").removeAttr('hidden');
    $(".port_view").attr('hidden', '');
}

var ee;
$(window).on("orientationchange", function(event) {
    ee = event;
    $(window).one('resize', resize_checker);

});

function resize_checker() {
    if (is_mobile === false) {
        show_chart();
        return;
    }

    if (window.matchMedia("(orientation: portrait)").matches) {
        // console.log("P");
        hide_chart();
    }
    if (window.matchMedia("(orientation: landscape)").matches) {
        // console.log("L");
        show_chart();

        if (chart_loaded === false) {
            load_chart();
        }
    }
}

function load_chart() {
    get_standings();
    chart_loaded = true;
}

var chart_loaded = false;
var is_mobile = false;

$(document).ready(function() {

    if( /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        is_mobile = true;
        resize_checker()
    }
    else {
        show_chart();
    }
    get_standings();

    // create_season_chart();

    console.log(is_mobile);

});