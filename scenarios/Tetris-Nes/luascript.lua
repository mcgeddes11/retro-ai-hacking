function spritemap_to_bool(input_val)
    -- sprite value 239 tells us the square is empty, anything else the square is occupied
    if input_val == 239 or input_val == nil then
        return 0
    else
        return 1
    end
end

function get_grid_state()
    -- function to take the 200 variables we're pulling from RAM and convert into a binary 20x10 array representation
    -- of the game state at any given time
    local gridstate
    -- pre allocate array
    gridstate = {}
    for rows = 1,20 do
        gridstate[rows] = {}
        for cols = 1,10 do
            gridstate[rows][cols] = 0
        end
    end
    -- TODO: fix this shit
    gridstate[20][1] = spritemap_to_bool(data.gridstate_r20c01)
    gridstate[20][2] = spritemap_to_bool(data.gridstate_r20c02)
    gridstate[20][3] = spritemap_to_bool(data.gridstate_r20c03)
    gridstate[20][4] = spritemap_to_bool(data.gridstate_r20c04)
    gridstate[20][5] = spritemap_to_bool(data.gridstate_r20c05)
    gridstate[20][6] = spritemap_to_bool(data.gridstate_r20c06)
    gridstate[20][7] = spritemap_to_bool(data.gridstate_r20c07)
    gridstate[20][8] = spritemap_to_bool(data.gridstate_r20c08)
    gridstate[20][9] = spritemap_to_bool(data.gridstate_r20c09)
    gridstate[20][10] = spritemap_to_bool(data.gridstate_r20c10)
    gridstate[19][1] = spritemap_to_bool(data.gridstate_r19c01)
    gridstate[19][2] = spritemap_to_bool(data.gridstate_r19c02)
    gridstate[19][3] = spritemap_to_bool(data.gridstate_r19c03)
    gridstate[19][4] = spritemap_to_bool(data.gridstate_r19c04)
    gridstate[19][5] = spritemap_to_bool(data.gridstate_r19c05)
    gridstate[19][6] = spritemap_to_bool(data.gridstate_r19c06)
    gridstate[19][7] = spritemap_to_bool(data.gridstate_r19c07)
    gridstate[19][8] = spritemap_to_bool(data.gridstate_r19c08)
    gridstate[19][9] = spritemap_to_bool(data.gridstate_r19c09)
    gridstate[19][10] = spritemap_to_bool(data.gridstate_r19c10)
    gridstate[18][1] = spritemap_to_bool(data.gridstate_r18c01)
    gridstate[18][2] = spritemap_to_bool(data.gridstate_r18c02)
    gridstate[18][3] = spritemap_to_bool(data.gridstate_r18c03)
    gridstate[18][4] = spritemap_to_bool(data.gridstate_r18c04)
    gridstate[18][5] = spritemap_to_bool(data.gridstate_r18c05)
    gridstate[18][6] = spritemap_to_bool(data.gridstate_r18c06)
    gridstate[18][7] = spritemap_to_bool(data.gridstate_r18c07)
    gridstate[18][8] = spritemap_to_bool(data.gridstate_r18c08)
    gridstate[18][9] = spritemap_to_bool(data.gridstate_r18c09)
    gridstate[18][10] = spritemap_to_bool(data.gridstate_r18c10)
    gridstate[17][1] = spritemap_to_bool(data.gridstate_r17c01)
    gridstate[17][2] = spritemap_to_bool(data.gridstate_r17c02)
    gridstate[17][3] = spritemap_to_bool(data.gridstate_r17c03)
    gridstate[17][4] = spritemap_to_bool(data.gridstate_r17c04)
    gridstate[17][5] = spritemap_to_bool(data.gridstate_r17c05)
    gridstate[17][6] = spritemap_to_bool(data.gridstate_r17c06)
    gridstate[17][7] = spritemap_to_bool(data.gridstate_r17c07)
    gridstate[17][8] = spritemap_to_bool(data.gridstate_r17c08)
    gridstate[17][9] = spritemap_to_bool(data.gridstate_r17c09)
    gridstate[17][10] = spritemap_to_bool(data.gridstate_r17c10)
    gridstate[16][1] = spritemap_to_bool(data.gridstate_r16c01)
    gridstate[16][2] = spritemap_to_bool(data.gridstate_r16c02)
    gridstate[16][3] = spritemap_to_bool(data.gridstate_r16c03)
    gridstate[16][4] = spritemap_to_bool(data.gridstate_r16c04)
    gridstate[16][5] = spritemap_to_bool(data.gridstate_r16c05)
    gridstate[16][6] = spritemap_to_bool(data.gridstate_r16c06)
    gridstate[16][7] = spritemap_to_bool(data.gridstate_r16c07)
    gridstate[16][8] = spritemap_to_bool(data.gridstate_r16c08)
    gridstate[16][9] = spritemap_to_bool(data.gridstate_r16c09)
    gridstate[16][10] = spritemap_to_bool(data.gridstate_r16c10)
    gridstate[15][1] = spritemap_to_bool(data.gridstate_r15c01)
    gridstate[15][2] = spritemap_to_bool(data.gridstate_r15c02)
    gridstate[15][3] = spritemap_to_bool(data.gridstate_r15c03)
    gridstate[15][4] = spritemap_to_bool(data.gridstate_r15c04)
    gridstate[15][5] = spritemap_to_bool(data.gridstate_r15c05)
    gridstate[15][6] = spritemap_to_bool(data.gridstate_r15c06)
    gridstate[15][7] = spritemap_to_bool(data.gridstate_r15c07)
    gridstate[15][8] = spritemap_to_bool(data.gridstate_r15c08)
    gridstate[15][9] = spritemap_to_bool(data.gridstate_r15c09)
    gridstate[15][10] = spritemap_to_bool(data.gridstate_r15c10)
    gridstate[14][1] = spritemap_to_bool(data.gridstate_r14c01)
    gridstate[14][2] = spritemap_to_bool(data.gridstate_r14c02)
    gridstate[14][3] = spritemap_to_bool(data.gridstate_r14c03)
    gridstate[14][4] = spritemap_to_bool(data.gridstate_r14c04)
    gridstate[14][5] = spritemap_to_bool(data.gridstate_r14c05)
    gridstate[14][6] = spritemap_to_bool(data.gridstate_r14c06)
    gridstate[14][7] = spritemap_to_bool(data.gridstate_r14c07)
    gridstate[14][8] = spritemap_to_bool(data.gridstate_r14c08)
    gridstate[14][9] = spritemap_to_bool(data.gridstate_r14c09)
    gridstate[14][10] = spritemap_to_bool(data.gridstate_r14c10)
    gridstate[13][1] = spritemap_to_bool(data.gridstate_r13c01)
    gridstate[13][2] = spritemap_to_bool(data.gridstate_r13c02)
    gridstate[13][3] = spritemap_to_bool(data.gridstate_r13c03)
    gridstate[13][4] = spritemap_to_bool(data.gridstate_r13c04)
    gridstate[13][5] = spritemap_to_bool(data.gridstate_r13c05)
    gridstate[13][6] = spritemap_to_bool(data.gridstate_r13c06)
    gridstate[13][7] = spritemap_to_bool(data.gridstate_r13c07)
    gridstate[13][8] = spritemap_to_bool(data.gridstate_r13c08)
    gridstate[13][9] = spritemap_to_bool(data.gridstate_r13c09)
    gridstate[13][10] = spritemap_to_bool(data.gridstate_r13c10)
    gridstate[12][1] = spritemap_to_bool(data.gridstate_r12c01)
    gridstate[12][2] = spritemap_to_bool(data.gridstate_r12c02)
    gridstate[12][3] = spritemap_to_bool(data.gridstate_r12c03)
    gridstate[12][4] = spritemap_to_bool(data.gridstate_r12c04)
    gridstate[12][5] = spritemap_to_bool(data.gridstate_r12c05)
    gridstate[12][6] = spritemap_to_bool(data.gridstate_r12c06)
    gridstate[12][7] = spritemap_to_bool(data.gridstate_r12c07)
    gridstate[12][8] = spritemap_to_bool(data.gridstate_r12c08)
    gridstate[12][9] = spritemap_to_bool(data.gridstate_r12c09)
    gridstate[12][10] = spritemap_to_bool(data.gridstate_r12c10)
    gridstate[11][1] = spritemap_to_bool(data.gridstate_r11c01)
    gridstate[11][2] = spritemap_to_bool(data.gridstate_r11c02)
    gridstate[11][3] = spritemap_to_bool(data.gridstate_r11c03)
    gridstate[11][4] = spritemap_to_bool(data.gridstate_r11c04)
    gridstate[11][5] = spritemap_to_bool(data.gridstate_r11c05)
    gridstate[11][6] = spritemap_to_bool(data.gridstate_r11c06)
    gridstate[11][7] = spritemap_to_bool(data.gridstate_r11c07)
    gridstate[11][8] = spritemap_to_bool(data.gridstate_r11c08)
    gridstate[11][9] = spritemap_to_bool(data.gridstate_r11c09)
    gridstate[11][10] = spritemap_to_bool(data.gridstate_r11c10)
    gridstate[10][1] = spritemap_to_bool(data.gridstate_r10c01)
    gridstate[10][2] = spritemap_to_bool(data.gridstate_r10c02)
    gridstate[10][3] = spritemap_to_bool(data.gridstate_r10c03)
    gridstate[10][4] = spritemap_to_bool(data.gridstate_r10c04)
    gridstate[10][5] = spritemap_to_bool(data.gridstate_r10c05)
    gridstate[10][6] = spritemap_to_bool(data.gridstate_r10c06)
    gridstate[10][7] = spritemap_to_bool(data.gridstate_r10c07)
    gridstate[10][8] = spritemap_to_bool(data.gridstate_r10c08)
    gridstate[10][9] = spritemap_to_bool(data.gridstate_r10c09)
    gridstate[10][10] = spritemap_to_bool(data.gridstate_r10c10)
    gridstate[9][1] = spritemap_to_bool(data.gridstate_r09c01)
    gridstate[9][2] = spritemap_to_bool(data.gridstate_r09c02)
    gridstate[9][3] = spritemap_to_bool(data.gridstate_r09c03)
    gridstate[9][4] = spritemap_to_bool(data.gridstate_r09c04)
    gridstate[9][5] = spritemap_to_bool(data.gridstate_r09c05)
    gridstate[9][6] = spritemap_to_bool(data.gridstate_r09c06)
    gridstate[9][7] = spritemap_to_bool(data.gridstate_r09c07)
    gridstate[9][8] = spritemap_to_bool(data.gridstate_r09c08)
    gridstate[9][9] = spritemap_to_bool(data.gridstate_r09c09)
    gridstate[9][10] = spritemap_to_bool(data.gridstate_r09c10)
    gridstate[8][1] = spritemap_to_bool(data.gridstate_r08c01)
    gridstate[8][2] = spritemap_to_bool(data.gridstate_r08c02)
    gridstate[8][3] = spritemap_to_bool(data.gridstate_r08c03)
    gridstate[8][4] = spritemap_to_bool(data.gridstate_r08c04)
    gridstate[8][5] = spritemap_to_bool(data.gridstate_r08c05)
    gridstate[8][6] = spritemap_to_bool(data.gridstate_r08c06)
    gridstate[8][7] = spritemap_to_bool(data.gridstate_r08c07)
    gridstate[8][8] = spritemap_to_bool(data.gridstate_r08c08)
    gridstate[8][9] = spritemap_to_bool(data.gridstate_r08c09)
    gridstate[8][10] = spritemap_to_bool(data.gridstate_r08c10)
    gridstate[7][1] = spritemap_to_bool(data.gridstate_r07c01)
    gridstate[7][2] = spritemap_to_bool(data.gridstate_r07c02)
    gridstate[7][3] = spritemap_to_bool(data.gridstate_r07c03)
    gridstate[7][4] = spritemap_to_bool(data.gridstate_r07c04)
    gridstate[7][5] = spritemap_to_bool(data.gridstate_r07c05)
    gridstate[7][6] = spritemap_to_bool(data.gridstate_r07c06)
    gridstate[7][7] = spritemap_to_bool(data.gridstate_r07c07)
    gridstate[7][8] = spritemap_to_bool(data.gridstate_r07c08)
    gridstate[7][9] = spritemap_to_bool(data.gridstate_r07c09)
    gridstate[7][10] = spritemap_to_bool(data.gridstate_r07c10)
    gridstate[6][1] = spritemap_to_bool(data.gridstate_r06c01)
    gridstate[6][2] = spritemap_to_bool(data.gridstate_r06c02)
    gridstate[6][3] = spritemap_to_bool(data.gridstate_r06c03)
    gridstate[6][4] = spritemap_to_bool(data.gridstate_r06c04)
    gridstate[6][5] = spritemap_to_bool(data.gridstate_r06c05)
    gridstate[6][6] = spritemap_to_bool(data.gridstate_r06c06)
    gridstate[6][7] = spritemap_to_bool(data.gridstate_r06c07)
    gridstate[6][8] = spritemap_to_bool(data.gridstate_r06c08)
    gridstate[6][9] = spritemap_to_bool(data.gridstate_r06c09)
    gridstate[6][10] = spritemap_to_bool(data.gridstate_r06c10)
    gridstate[5][1] = spritemap_to_bool(data.gridstate_r05c01)
    gridstate[5][2] = spritemap_to_bool(data.gridstate_r05c02)
    gridstate[5][3] = spritemap_to_bool(data.gridstate_r05c03)
    gridstate[5][4] = spritemap_to_bool(data.gridstate_r05c04)
    gridstate[5][5] = spritemap_to_bool(data.gridstate_r05c05)
    gridstate[5][6] = spritemap_to_bool(data.gridstate_r05c06)
    gridstate[5][7] = spritemap_to_bool(data.gridstate_r05c07)
    gridstate[5][8] = spritemap_to_bool(data.gridstate_r05c08)
    gridstate[5][9] = spritemap_to_bool(data.gridstate_r05c09)
    gridstate[5][10] = spritemap_to_bool(data.gridstate_r05c10)
    gridstate[4][1] = spritemap_to_bool(data.gridstate_r04c01)
    gridstate[4][2] = spritemap_to_bool(data.gridstate_r04c02)
    gridstate[4][3] = spritemap_to_bool(data.gridstate_r04c03)
    gridstate[4][4] = spritemap_to_bool(data.gridstate_r04c04)
    gridstate[4][5] = spritemap_to_bool(data.gridstate_r04c05)
    gridstate[4][6] = spritemap_to_bool(data.gridstate_r04c06)
    gridstate[4][7] = spritemap_to_bool(data.gridstate_r04c07)
    gridstate[4][8] = spritemap_to_bool(data.gridstate_r04c08)
    gridstate[4][9] = spritemap_to_bool(data.gridstate_r04c09)
    gridstate[4][10] = spritemap_to_bool(data.gridstate_r04c10)
    gridstate[3][1] = spritemap_to_bool(data.gridstate_r03c01)
    gridstate[3][2] = spritemap_to_bool(data.gridstate_r03c02)
    gridstate[3][3] = spritemap_to_bool(data.gridstate_r03c03)
    gridstate[3][4] = spritemap_to_bool(data.gridstate_r03c04)
    gridstate[3][5] = spritemap_to_bool(data.gridstate_r03c05)
    gridstate[3][6] = spritemap_to_bool(data.gridstate_r03c06)
    gridstate[3][7] = spritemap_to_bool(data.gridstate_r03c07)
    gridstate[3][8] = spritemap_to_bool(data.gridstate_r03c08)
    gridstate[3][9] = spritemap_to_bool(data.gridstate_r03c09)
    gridstate[3][10] = spritemap_to_bool(data.gridstate_r03c10)
    gridstate[2][1] = spritemap_to_bool(data.gridstate_r02c01)
    gridstate[2][2] = spritemap_to_bool(data.gridstate_r02c02)
    gridstate[2][3] = spritemap_to_bool(data.gridstate_r02c03)
    gridstate[2][4] = spritemap_to_bool(data.gridstate_r02c04)
    gridstate[2][5] = spritemap_to_bool(data.gridstate_r02c05)
    gridstate[2][6] = spritemap_to_bool(data.gridstate_r02c06)
    gridstate[2][7] = spritemap_to_bool(data.gridstate_r02c07)
    gridstate[2][8] = spritemap_to_bool(data.gridstate_r02c08)
    gridstate[2][9] = spritemap_to_bool(data.gridstate_r02c09)
    gridstate[2][10] = spritemap_to_bool(data.gridstate_r02c10)
    gridstate[1][1] = spritemap_to_bool(data.gridstate_r01c01)
    gridstate[1][2] = spritemap_to_bool(data.gridstate_r01c02)
    gridstate[1][3] = spritemap_to_bool(data.gridstate_r01c03)
    gridstate[1][4] = spritemap_to_bool(data.gridstate_r01c04)
    gridstate[1][5] = spritemap_to_bool(data.gridstate_r01c05)
    gridstate[1][6] = spritemap_to_bool(data.gridstate_r01c06)
    gridstate[1][7] = spritemap_to_bool(data.gridstate_r01c07)
    gridstate[1][8] = spritemap_to_bool(data.gridstate_r01c08)
    gridstate[1][9] = spritemap_to_bool(data.gridstate_r01c09)
    gridstate[1][10] = spritemap_to_bool(data.gridstate_r01c10)
    return gridstate
end

function is_hole(grid_state, row, col)
    local tf = true
    if grid_state[row][col] ~= 0 or row == 20 then
        return false
    else
        if grid_state[row-1][col] == 1
            and grid_state[row-1][col-1] == 1
            and grid_state[row-1][col+1] == 1
            and grid_state[row][col-1] == 1
            and grid_state[row][col+1] == 1
            and grid_state[row+1][col-1] == 1
            and grid_state[row+1][col] == 1
            and grid_state[row+1][col+1] == 1 then
            return true
        else
            return false
        end
    end
end



function compute_bumpiness(grid_state)
    local bumpiness = 0
    local row, col, this_col_max_row, last_col_max_row
    for col = 1, 10 do
        this_col_max_row = 0
        for row = 1, 20 do
            if grid_state[row][col] == 1 and row > this_col_max_row then
                this_col_max_row = row
            end
        end
        if col > 1 then
            bumpiness = bumpiness + math.abs(this_col_max_row - last_col_max_row)
        end
        last_col_max_row = this_col_max_row
    end
    return bumpiness
end

function count_holes(grid_state)
    local hole_count = 0
--    local row, col
--    for row = 1,20 do
--        for col = 1,10 do
--            if is_hole(grid_state, row, col) then
--                hole_count = hole_count + 1
--            end
--        end
--    end
    return hole_count
end

function compute_aggregate_height(grid_state)
    local aggregate_height = 0
    local row, col, max_row
    for col = 1, 10 do
        max_row = 0
        for row = 1, 20 do
            if grid_state[row][col] == 1 and row > max_row then
                max_row = row
            end
        end
        aggregate_height = aggregate_height + max_row
    end
    return aggregate_height
end

function done_check()
    local grid_state, height
    if data.game_over == 10 then
        return true
    else
        return false
    end
end


previous_reward = 0

function compute_reward()
    local reward, height, hole_count, bumpiness, delta, grid_state, step_reward
    if done_check() then
        return 0
    end

--    grid_state = get_grid_state()
--    height = compute_aggregate_height(grid_state)
--    bumpiness = compute_bumpiness(grid_state)
--    hole_count = count_holes(grid_state)

--    reward = 7.6 * data.lines - 5.1 * height - 3.5 * holes - 1.8 * bumpiness
--    reward = 7.6 * data.lines - 5.1 * height - 1.8 * bumpiness
--    delta = reward - previous_reward
--    previous_reward = reward
    if data.lines > previous_reward then
        step_reward = data.lines - previous_reward
        previous_reward = data.lines
    else
        step_reward = 0
    end
    return step_reward
end