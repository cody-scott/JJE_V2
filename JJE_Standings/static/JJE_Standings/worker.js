var base_url = location["protocol"] + "//" + location["host"] + "/";
var standings_api = base_url + "api/";
var current_standings_url = standings_api + "current_standings/";
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
var raw_as;

function get_standings() {
    $.getJSON(
        current_standings_url + "?format=json", function(data) {
            standings_data = process_data(data);

            for (var i=0; i<data.length; i++) {
                var tm = data[i]['team_name'];
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
            raw_as = data;
            all_standings_data = process_all_standings(data);
            create_season_chart();
        }
    )
}

function load_standings() {
    get_all_standings();
}

function process_data(data) {
    var dt = [];
    var lbl = [];
    for (var i=0; i < data.length; i++) {
        var current_team = data[i];
        lbl.push(current_team['team_name']);
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
    var out_data = []
    for (var i=0; i< data.length; i++) {
        var c_row = data[i];
        var tm = c_row['team_name'];
        var standings = c_row['standing_team'].sort((a, b) => (a.standings_week > b.standings_week) ? 1: -1);

        var standing_dict = {
            'label': tm,
            'borderColor': team_colors[tm],
            'backgroundColor': team_colors[tm],
            'fill': false,
            'data': standings.map((val) => ({"x": "Week " + val.standings_week, "y": val.stat_point_total}))
        }
        out_data.push(standing_dict)
    }
    return out_data;
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
    console.log(is_mobile);
});