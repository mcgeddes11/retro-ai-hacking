--
-- Created by IntelliJ IDEA.
-- User: joncocks
-- Date: 2021-01-26
-- Time: 9:50 p.m.
-- To change this template use File | Settings | File Templates.
--

frames_since_checkpoint_update = 0
previous_global_checkpoint = 0

function get_global_checkpoint()
    local global_checkpoint, lap_number
    lap_number = get_lap_number()
    global_checkpoint = (lap_number * data.lapsize) + data.checkpoint
    return global_checkpoint
end

function done_check()
    local clock_seconds
    clock_seconds = get_clock_seconds()
    -- if any of following are true, end
    -- race is over
    -- more than CHECKPOINT_UPDATE_BUFFER seconds and checkpoint hasn't updated
    CHECKPOINT_UPDATE_BUFFER = 300
    if data.lapnumber_code == 133 or clock_seconds > 120 or frames_since_checkpoint_update > CHECKPOINT_UPDATE_BUFFER or data.flow ~= 0 then
        return true
    else
        return false
    end
end

function is_gameplay()
	local lap
    lap = get_lap_number()
	if lap >= 5 then
		return false
	end
	if lap < 0 then
		return false
	end
	return true
end


function get_clock_seconds()
    local clock_seconds, clock_minutes
    if data.clock < 1000000 then
        clock_seconds = math.floor(data.clock / 100)
        clock_minutes = 0
    else
        clock_minutes = math.floor(data.clock / 1e6)
        clock_seconds = math.floor((data.clock % 1e6) / 100)
    end
    return clock_seconds + 60 * clock_minutes
end

function compute_actual_field_position()
    -- this is stored in RAM as (rank-1) * 2, so let's convert it back to actual rank
    local rank
    rank = (data.field_position / 2) + 1
    return rank
end

function get_lap_number()
    local lap_number
    return data.lapnumber_code - 128
end

function compute_reward()
    local total_reward, global_checkpoint, checkpoint_reward, speed_reward, surface_reward, backward_penalty
    total_reward = 0

--    if not is_gameplay() then
--        return 0
--    end

    -- Checkpoint rewards
    global_checkpoint = get_global_checkpoint()
    checkpoint_reward = 100 * (global_checkpoint - previous_global_checkpoint)
    -- Update previous global checkpoint
    if global_checkpoint ~= previous_global_checkpoint then
        previous_global_checkpoint = global_checkpoint
        frames_since_checkpoint_update = 0
    else
        frames_since_checkpoint_update = frames_since_checkpoint_update + 1
    end
    -- Speed reward
    if data.speed > 100 then
        speed_reward = 0.5
    else
        speed_reward = 0
    end
    -- Surface reward
    if data.surface_type_code == 40 then
        surface_reward = 0
    else
        surface_reward = -1.0
    end


    total_reward = speed_reward + checkpoint_reward + surface_reward
--    total_reward = checkpoint_reward
    return total_reward
end
