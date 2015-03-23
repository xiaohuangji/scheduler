// The grid manages tiles using ids, which you can define. For our
// examples we'll just use the tile number as the unique id.
var TILE_IDS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31
];


// debounce utility from underscorejs.org
function debounce(func, wait, immediate) {
    var timeout;
    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        if (immediate && !timeout) func.apply(context, args);
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


// function returns a Tiles.js template for job records
// template contains tiles_number of tiles
// each tile has proportion 3x2 (wider than taller)
function grid_info_template(tiles_number) {
    var arr = [];
    for (var i = 0; i < tiles_number; i++) {
        if (i % 2 == 0) {
            arr.push(" A A A ");
            arr.push(" A A A ");
        } else {
            arr.push(" B B B ");
            arr.push(" B B B ");
        }
    }
    return arr;
}


var GridHeaderTemplate = [" . "];


function header_tree_tile(mx_tree, tile) {
    tile.$el.append('<div class="dev-tile-content">Tree Name</div>'
        + '<div class="dev-tile-content">' + mx_tree.tree_name + '</div>'
        + '<div class="dev-tile-content">Dependent On</div>'
        + '<div class="dev-tile-content">' + mx_tree.dependent_on + '</div>'
        + '<div class="dev-tile-content">Dependant Trees</div>'
        + '<div class="dev-tile-content">' + mx_tree.dependant_trees + '</div>');
}


function header_process_tile(process_entry, tile) {
    tile.$el.append('<div class="dev-tile-content">Trigger On/Alive</div>'
        + '<div class="dev-tile-content">' + process_entry.is_on + '/' + process_entry.is_alive + '</div>'
        + '<div class="dev-tile-content">Process Name</div>'
        + '<div class="dev-tile-content">' + process_entry.process_name + '</div>'
        + '<div class="dev-tile-content">Next Timeperiod</div>'
        + '<div class="dev-tile-content">' + process_entry.next_timeperiod + '</div>'
        + '<div class="dev-tile-content">Next Run In</div>'
        + '<div class="dev-tile-content">' + process_entry.next_run_in + '</div>'
        + '<div class="dev-tile-content">' + 'Trigger Now Button' + '</div>'
        + '<div class="dev-tile-content">Reprocessing Queue</div>'
        + '<div class="dev-tile-content">' + process_entry.reprocessing_queue + '</div>');
}


function info_process_tile(process_entry, tile) {
    tile.$el.append('<div class="dev-tile-content">Process Name</div>'
        + '<div class="dev-tile-content">' + process_entry.process_name + '</div>'
        + '<div class="dev-tile-content">Time Qualifier</div>'
        + '<div class="dev-tile-content">' + process_entry.time_qualifier + '</div>'
        + '<div class="dev-tile-content">State Machine</div>'
        + '<div class="dev-tile-content">' + process_entry.state_machine + '</div>'
        + '<div class="dev-tile-content">Blocking type</div>'
        + '<div class="dev-tile-content">' + process_entry.blocking_type + '</div>'
        + '<div class="dev-tile-content">Run On Active Timeperiod</div>'
        + '<div class="dev-tile-content">' + process_entry.run_on_active_timeperiod + '</div>'
        + '<div class="dev-tile-content">Trigger Frequency</div>'
        + '<input type="text" size="8" maxlength="32" name="interval" value="' + process_entry.trigger_frequency + '" />');
}


function info_job_tile(job_entry, tile) {
    var checkbox_value = "{ process_name: '" + job_entry.process_name + "', timeperiod: '" + job_entry.timeperiod + "' }";
    var checkbox_div = '<input type="checkbox" name="batch_processing" value="' + checkbox_value + '"/>';

    var uow_button = $('<button>Get&nbsp;Uow</button>').click(function (e) {
        var params = { action: 'action_get_uow', timeperiod: job_entry.timeperiod, process_name: job_entry.process_name };
        var viewer_url = '/object_viewer/?' + $.param(params);
        window.open(viewer_url, 'Object Viewer', 'width=400,height=350,screenX=400,screenY=200,scrollbars=1');
    });
    var log_button = $('<button>View&nbsp;Log</button>').click(function (e) {
        var params = { action: 'action_get_log', timeperiod: job_entry.timeperiod, process_name: job_entry.process_name };
        var viewer_url = '/object_viewer/?' + $.param(params);
        window.open(viewer_url, 'Object Viewer', 'width=720,height=480,screenX=400,screenY=200,scrollbars=1');
    });

    tile.$el.attr('class', job_entry.state);
    tile.$el.append($('<div></div>').append(checkbox_div).append(' p/t: ' + job_entry.process_name + '/' + tile.id));
    tile.$el.append('<div class="dev-title-content">timeperiod: ' + job_entry.timeperiod + '</div>'
            + '<div class="dev-title-content">state: ' + job_entry.state + '</div>'
            + '<div class="dev-title-content">#fails: ' + job_entry.num_failed + '</div>'
    );
    tile.$el.append($('<div></div>').append(uow_button));
    tile.$el.append($('<div></div>').append(log_button));
}


var mx_trees = {
    'TreeSite': {'tree_name': 'TreeSite',
        'dependent_on': [],
        'dependant_trees': [],
        'processes': ['SiteYearly', 'SiteMonthly', 'SiteDaily', 'SiteHourly']},
    'TreeAlert': {'tree_name': 'TreeAlert',
        'dependent_on': [],
        'dependant_trees': [],
        'processes': ['AlertDaily']}
};


function get_process_entry(process_name) {
    return {
        'process_name': process_name,
        'is_on': true,
        'is_alive': true,
        'next_timeperiod': '2019098822',
        'next_run_in': '25:10',
        'reprocessing_queue': [],
        'time_qualifier': '_hourly',
        'state_machine': 'descrete',
        'blocking_type': 'blocking_children',
        'run_on_active_timeperiod': false,
        'trigger_frequency': 'every 600 sec'
    };
}


function get_job_record(process_name) {
    return {
        'process_name': process_name,
        'timeperiod': '2019098822',
        'state': 'state_in_progress',
        'num_failed': 10
    };
}


function build_grid(grid_name, grid_template, builder_function, info_obj) {
    var el = document.getElementById(grid_name);
    var grid = new Tiles.Grid(el);

    // template is selected by user, not generated so just
    // return the number of columns in the current template
    grid.resizeColumns = function () {
        return this.template.numCols;
    };

    // by default, each tile is an empty div, we'll override creation
    // to add a tile number to each div
    grid.createTile = function (tileId) {
        var tile = new Tiles.Tile(tileId);
        builder_function(info_obj, tile);
        return tile;
    };

    // set the new template and resize the grid
    grid.template = Tiles.Template.fromJSON(grid_template);
    grid.isDirty = true;
    grid.resize();

    // adjust number of tiles to match selected template
    var ids = TILE_IDS.slice(0, grid.template.rects.length);
    grid.updateTiles(ids);
    grid.redraw(true);
}


$(function () {
    for (var tree_name in mx_trees) {
        var tree_obj = mx_trees[tree_name];
        var grid_name;
        var builder_function;
        var info_obj;
        var process_name;

        // *** HEADER ***
        build_grid("grid-header-" + tree_obj.tree_name, GridHeaderTemplate, header_tree_tile, tree_obj);

        var p_length = tree_obj.processes.length;
        for (var i = 0; i < p_length; i++) {
            process_name = tree_obj.processes[i];
            build_grid("grid-header-" + process_name, GridHeaderTemplate, header_process_tile, get_process_entry(process_name));
        }


        // *** INFO ***
        for (var j = 0; j < p_length; j++) {
            process_name = tree_obj.processes[j];
            build_grid("grid-info-" + tree_obj.tree_name, grid_info_template(p_length), info_process_tile, get_process_entry(process_name));

            var j_length = 10;
            for (var k = 0; k < j_length; k++) {
                build_grid("grid-info-" + process_name, grid_info_template(j_length), info_job_tile, get_job_record(process_name));
            }
        }
    }

    // wait until users finishes resizing the browser
    var debounced_resize = debounce(function () {
        grid.resize();
        grid.redraw(true);
    }, 200);

    // when the window resizes, redraw the grid
    $(window).resize(debounced_resize);
});
