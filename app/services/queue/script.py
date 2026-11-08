MATCH_OR_QUEUE_SCRIPT = """
local queue_key = KEYS[1]
local queued_key = KEYS[2]
local active_key = KEYS[3]

local user_id = ARGV[1]

-- Проверяем, не находится ли пользователь в диалоге
if redis.call('SISMEMBER', active_key, user_id) == 1 then
    return { "already_active", "" }
end

-- Проверяем, не стоит ли уже пользователь в очереди
if redis.call('SISMEMBER', queued_key, user_id) == 1 then
    return { "already_queued", "" }
end

-- Ищем свободного собеседника
while redis.call('LLEN', queue_key) > 0 do
    local partner_id = redis.call('LPOP', queue_key)

    redis.call('SREM', queued_key, partner_id)

    -- Защита от самоматчинга и пользователей,
    -- которые уже находятся в диалоге
    if partner_id ~= user_id
        and redis.call('SISMEMBER', active_key, partner_id) == 0 then

        return { "matched", partner_id }
    end
end

-- Никого не нашли — ставим пользователя в очередь
redis.call('RPUSH', queue_key, user_id)
redis.call('SADD', queued_key, user_id)

return { "queued", "" }
"""
