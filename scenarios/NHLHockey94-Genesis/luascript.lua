-- TODO: make this support playing more than just first period
-- Constants
oz_blueline_y_pos = 80
dz_blueline_y_pos = -80
-- these clock values are used in a couple of places
-- represents the number of time steps in a period at different speeds
max_clock_at_fast = 300
max_clock_at_normal = 600
-- positions of net in oz/dz/
oz_net_pos_x = 0
oz_net_pos_y = 265
dz_net_pos_x = 0
dz_net_pos_y = -265
-- frames beyond which, if the clock hasn't changed, we determine a stoppage
clock_stop_frame_buffer = 30
-- euclidean distance in pixel space to determine whether we have possession of the puck
puck_possession_dist_threshold = 15

-- Reward multipliers
-- position of puck in zone (OZ positive, DZ negative, NZ zero)
zone_multiplier = 1
-- distance of puck to net, inverse multiplier (OZ positive, DZ negative, NZ zero)
dist_to_net_multiplier = 2
-- multiplier for having possession of puck
possession_multiplier = 3
-- reward for maintaining a positive shot differential (ie. shots_for - shots_against)
shot_differential_multiplier = 4
-- likewise, but for score effects (ie. score_for - score_against)
lead_multiplier = 6
-- instantaneous reward for generating a **VALID** shot on net
shot_multiplier = 10
-- instantaneous reward for scoring a goal (penalty for goal against)
goal_multiplier = 20

-- Keeping track of previous states
previous_reward = 0
previous_goals_for = 0
previous_shots_for = 0
previous_shots_against = 0
previous_goals_against = 0
frames_since_last_clock_update = 0
previous_clock = max_clock_at_fast
clock_is_stopped = false

-- we note that simply giving benefit for shots encourages AI to take wildly unsuccessful shots from deep in DZ/NZ.
-- We need to adjust so that the shots reward is only given for shots taken in OZ. We apply this logic to shot differential
-- (ie. maintaining a lead) reward as well as instantaneous reward for taking a shot on net. Penalties for shots against
-- aren't adjusted
adjusted_shots_for = 0

function bool_to_number(bool_val)
    if bool_val == true then
        return 1
    else
        return 0
    end
end

function done_check()
    -- this function encapsulates the code determining when an episode is over
    if data.clock == 0 then
        return true
    else
        return false
    end
end

function dist_player_to_puck()
    -- compute distance from the current active player to the puck
    local dist
    dist = math.sqrt((data.focus_player_position_x - data.puck_position_x)^2 + (data.focus_player_position_y - data.puck_position_y)^2)
    return dist
end

function player_has_possession(dist_to_puck)
    -- determine, based on distance to puck, if this player has possession
    -- TODO: this is a bit unreliable, would be better to find a RAM value for this
    if dist_to_puck < puck_possession_dist_threshold then
        return true
    else
        return false
    end
end

function dist_puck_to_net(net_pos_x, net_pos_y)
    -- compute euclidean distance in pixel-space from puck to net
    local dist
    dist = math.sqrt((net_pos_x - data.puck_position_x)^2 + (net_pos_y - data.puck_position_y)^2)
    return dist
end

function object_is_in_dz(y_pos)
    -- return whether an object is in DZ
    return y_pos < dz_blueline_y_pos
end

function object_is_in_oz(y_pos)
    -- return whether object is in OZ
    -- TODO: this needs to change if we support playing more than first period
    return y_pos > oz_blueline_y_pos
end

function update_clock()
    -- this function performs a check on the current and previous state of the clock
    -- it's used primarily to determine stoppages, as we don't want to reward anything when the clock is stopped
    -- if the clock hasn't moved since last frame, increment the frames_since_last_clock_update counter
    -- if it has moved since last frame, reset the frame counter and update the previous clock value
    if data.clock == previous_clock then
        frames_since_last_clock_update = frames_since_last_clock_update + 1
    else
        frames_since_last_clock_update = 0
        previous_clock = data.clock
    end
end

function clock_is_stopped()
    -- determine if clock is stopped
    if frames_since_last_clock_update > clock_stop_frame_buffer then
        return true
    else
        return false
    end
end

function compute_adjusted_shots_for()
    -- check whether a shot has been generated in the current frame
    if data.shots_for > previous_shots_for then
        -- check for valid OZ positioning.  This is a bit of a hack, in order for a shot to be "VALID" it must occur
        -- when currently focused player is in the OZ. This is to discourage wild shots from outside NZ/DZ. could use a
        -- distance to net filter, but let's start simple. If so, increment the adjusted_shots_for counter.
        if object_is_in_oz(data.focus_player_position_y) then
            adjusted_shots_for = adjusted_shots_for + 1
        end
        -- Regardless, we need to update the previous_shots_for value
        previous_shots_for = data.shots_for
    end
end


function compute_reward()
    local dist_to_puck, has_possession, puck_in_oz, puck_in_dz, dist_to_net_oz, dist_to_net_dz, reward_shot_differential,
    reward_goal_differential, reward_possession, reward_zone, reward_dist_to_net, step_reward, reward_delta, player_in_oz, player_in_dz,
    reward_instantaneous_shot, reward_instantaneous_goal
    -- return zero if we're done
    if done_check() then
        return 0
    end

    -- Figure out if the clock is stopped. If so, reward zero.
    update_clock()
    if clock_is_stopped() then
        return 0
    end

    -- find distance from active player to the puck
    dist_to_puck = dist_player_to_puck()
    -- determine whether we have possession - this is kinda rough
    has_possession = player_has_possession(dist_to_puck)
    -- is the puck in OZ or DZ?
    puck_in_oz = object_is_in_oz(data.puck_position_y)
    puck_in_dz = object_is_in_dz(data.puck_position_y)
    -- is the active player in the OZ?
    player_in_oz = object_is_in_oz(data.focus_player_position_y)

    -- find distance to oz/dz net
    dist_to_net_oz = dist_puck_to_net(oz_net_pos_x, oz_net_pos_y)
    dist_to_net_dz = dist_puck_to_net(dz_net_pos_x, dz_net_pos_y)

    -- compute reward components
    -- Goals - bonus for maintaining a lead
    -- TODO: is this useful?
    reward_goal_differential = lead_multiplier * (data.score1 - data.score2)
    -- Shots - bonus for maintaining shot differential (note we're using adjusted shots for here)
    -- TODO: is this useful?
    reward_shot_differential = shot_differential_multiplier * (data.shots_for - data.shots_against)
    -- OZ/DZ and distance to net, including possession
    if puck_in_oz then
        -- in OZ we don't wanna penalize not having possession due to passing
        if has_possession then
            reward_possession = possession_multiplier
        else
            reward_possession = 0
        end
        reward_zone = zone_multiplier
        reward_dist_to_net = dist_to_net_multiplier * 1/dist_to_net_oz
    elseif puck_in_dz then
        -- this asymmetric reward is intended to encourage getting possession of the puck in the DZ
        if has_possession then
            reward_possession = possession_multiplier
        else
            reward_possession = -possession_multiplier
        end
        reward_zone = -zone_multiplier
        reward_dist_to_net = -dist_to_net_multiplier * 1/dist_to_net_dz
    else
        -- in the NZ reward possession, do not penalize losing the puck
        if has_possession then
            reward_possession = possession_multiplier
        else
            reward_possession = 0
        end
        reward_zone = 0
        reward_dist_to_net = 0
    end

    -- instantaneous rewards for shots/goals for/against
    if data.shots_for > previous_shots_for then
        previous_shots_for = data.shots_for
        if object_is_in_oz(data.focus_player_position_y) then
            reward_instantaneous_shot = shot_multiplier
        else
            reward_instantaneous_shot = 0
        end
    else
        reward_instantaneous_shot = 0
    end

    if data.score1 > previous_goals_for then
        previous_goals_for = data.score1
        reward_instantaneous_goal = goal_multiplier
    else
        reward_instantaneous_goal = 0
    end

    -- instantaneous rewards for shots/goals for/against
    if data.shots_against > previous_shots_against then
        previous_shots_against = data.shots_against
        reward_instantaneous_shot = -shot_multiplier
    else
        reward_instantaneous_shot = 0
    end

    if data.score2 > previous_goals_for then
        previous_goals_against = data.score2
        reward_instantaneous_goal = -goal_multiplier
    else
        reward_instantaneous_goal = 0
    end



    -- compute final reward
--    step_reward = reward_goal_differential + reward_shot_differential + reward_possession + reward_zone + reward_dist_to_net + reward_instantaneous_goal + reward_instantaneous_shot
    step_reward = reward_possession + reward_zone + reward_dist_to_net + reward_instantaneous_goal + reward_instantaneous_shot
    -- compute delta
    reward_delta = step_reward - previous_reward
    -- return delta as reward
    return reward_delta

end