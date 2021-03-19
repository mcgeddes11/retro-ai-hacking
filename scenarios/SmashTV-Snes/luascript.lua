--
-- Created by IntelliJ IDEA.
-- User: joncocks
-- Date: 2021-01-26
-- Time: 9:50 p.m.
-- To change this template use File | Settings | File Templates.
--

previous_score = 0
previous_lives = 5

function done_check()
    local clock_seconds
    if data.lives == 0 then
        return true
    else
        return false
    end
end



function compute_reward()
    local score_reward, score_diff, death_penalty, lives_diff
    score_diff = data.score - previous_score
    lives_diff = previous_lives - data.lives
    score_reward = score_diff
    death_penalty = -1000 * lives_diff
    previous_score = data.score
    previous_lives = data.lives
    return score_reward + death_penalty
end