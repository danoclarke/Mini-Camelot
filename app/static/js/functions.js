$(document).on("ready",function(){
    w = $('.note').width();

    d3.select('.whitesel').attr("cx",w/4);
    d3.select('.blacksel').attr("cx",3*w/4);
})

$(document).on("click",".whitesel",function(){
    player_num = 1;
    d3.select('.note').style('display','none');
    d3.selectAll('.piece.white').style("cursor","pointer");
});
$(document).on("click",".blacksel",function(){
    player_num = -1;
    d3.select('.note').style('display','none');
    d3.selectAll('.piece.black').style("cursor","pointer");
    //Run CPU Move
    $.ajax({
        type: 'GET',
        data: {'payload': JSON.stringify({'board':board,'player':-player_num})},
        contentType: "application/json",
        url: 'cpu_move',
        success: function(response) {
            data = JSON.parse(response);

            $('.info').html('Number of Nodes Generated: ' + data['num_nodes'] + '<br/>' + 'Max. Depth Reached: ' + data['max_d'] + '<br/>' + 'Max-Node Prunes: ' + data['max_node_prunes'] + '<br/>' + 'Min-Node Prunes: ' + data['min_node_prunes']);

            var sel = d3.select('.piece.id' + data['move'][0]);

            var x_loc = d3.select('.place.id' + data['move'][1]).attr("cx");
            var y_loc = d3.select('.place.id' + data['move'][1]).attr("cy");

            sel.attr("cx",x_loc).attr("cy",y_loc).attr("id",data['move'][1])
                .classed("id"+data['move'][0], false)
                .classed("id"+data['move'][1], true);

            if(data['move'].length > 2){
                d3.select(".piece.id" + data['move'][2]).remove();
            }


            update_board();
        },
    });
});

var moving_piece = false;
var glob_all_possible_moves = [];
var glob_possible_moves = [];
var glob_remove_list = [];

var game_over = false;

function update_board(){
    //Update Board
    white_ps = [];
    black_ps = [];

    $('.white.piece').each(function(index){
        var id = $(this).attr("id");
        white_ps.push(parseInt(id));
    });

    $('.black.piece').each(function(index){
        var id = $(this).attr("id");
        black_ps.push(parseInt(id));
    });

    board = {'white':white_ps,'black':black_ps,'emptys':emptys};

    black_winners = [3,4];
    white_winners = [107,108];

    black_winners.forEach(function(c){
        if(black_ps.indexOf(c) > -1){
            d3.select('.note').html('Team Black Wins!').style('display','block').style('opacity','1');
            game_over = true;
        }
    });

    white_winners.forEach(function(c){
        if(white_ps.indexOf(c) > -1){
            d3.select('.note').html('Team Black Wins!').style('display','block').style('opacity','1');
            game_over = true;
        }
    });
}

if(!game_over){
    $(document).on("click",".piece",function(){
        var all_possible_moves = [];
        var possible_moves = [];
        var remove_list = [];

        if(!moving_piece){
            moving_piece = true;
            d3.select(this).classed("selected",true);
            var id = d3.select(this).attr("id");
        }else{
            d3.select(".piece.selected").classed("selected",false);
            d3.select(this).classed("selected",true);
            var id = d3.select(this).attr("id");
        }

        $.ajax({
            type: 'GET',
            data: {'payload': JSON.stringify({'board':board,'player':player_num})},
            contentType: "application/json",
            url: 'poss_move',
            success: function(response) {
                all_possible_moves = JSON.parse(response);

                all_possible_moves.forEach(function(move){
                    if(move[0] == parseInt(id)){
                        possible_moves.push(move[1]);
                    }
                    if(move.length == 3){
                        remove_list.push(move[2]);
                    }
                });

                d3.selectAll('.place').style("fill","#fff");
                d3.selectAll('.piece').style("stroke","#ddd").style("stroke-width","4");

                possible_moves.forEach(function(i){
                    d3.select('.place.id' + i)
                    .style("fill","rgba(255,0,0,0.2)");
                });

                remove_list.forEach(function(i){
                    d3.select('.piece.id' + i)
                    .style("stroke","rgba(255,0,0,0.2)")
                    .style("stroke-width","4");
                });

                glob_possible_moves = possible_moves;
                glob_remove_list = remove_list;
            },
        });
    });

    $(document).on("click",".place",function(){
        var id_loc = d3.select(this).attr("id")
        var x_loc = d3.select(this).attr("cx");
        var y_loc = d3.select(this).attr("cy");
        
        if(moving_piece && glob_possible_moves.indexOf(parseInt(id_loc)) > -1){
            var sel = d3.select(".piece.selected");
            var old_id = sel.attr("id");

            sel.transition().duration(500).attr("cx",x_loc).attr("cy",y_loc);

            sel.attr("id",id_loc)
                .classed('id'+old_id,false)
                .classed('id'+id_loc,true);

            if(glob_remove_list.length > 0){
                d3.select(".piece.id" + glob_remove_list[0]).remove();
            }

            moving_piece = false;
            d3.select(".piece.selected").classed("selected",false);

            d3.selectAll('.place').style("fill","#fff");


            update_board();

            if(!game_over){
                //Run CPU Move
                $.ajax({
                    type: 'GET',
                    data: {'payload': JSON.stringify({'board':board,'player':-player_num})},
                    contentType: "application/json",
                    url: 'cpu_move',
                    success: function(response) {
                        data = JSON.parse(response);

                        $('.info').html('Number of Nodes Generated: ' + data['num_nodes'] + '<br/>' + 'Max. Depth Reached: ' + data['max_d'] + '<br/>' + 'Max-Node Prunes: ' + data['max_node_prunes'] + '<br/>' + 'Min-Node Prunes: ' + data['min_node_prunes']);

                        var sel = d3.select('.piece.id' + data['move'][0]);

                        var x_loc = d3.select('.place.id' + data['move'][1]).attr("cx");
                        var y_loc = d3.select('.place.id' + data['move'][1]).attr("cy");

                        sel.transition().duration(500).attr("cx",x_loc).attr("cy",y_loc)
                        sel.attr("id",data['move'][1])
                            .classed("id"+data['move'][0], false)
                            .classed("id"+data['move'][1], true);

                        if(data['move'].length > 2){
                            d3.select(".piece.id" + data['move'][2]).remove();
                        }


                        update_board();
                    },
                });
            }
        }
    });
}