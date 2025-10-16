-- Initialize database for subscription and payment system

-- Create subscription_payments table
CREATE TABLE IF NOT EXISTS subscription_payments (
    id VARCHAR(26) PRIMARY KEY,
    user_id VARCHAR(26) NOT NULL,
    subscription_tier VARCHAR(20) NOT NULL,
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    transaction_id VARCHAR(255) UNIQUE,
    processed_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata_json JSONB
);

-- Create indexes for subscription_payments
CREATE INDEX IF NOT EXISTS idx_subscription_payments_user_id ON subscription_payments(user_id);
CREATE INDEX IF NOT EXISTS idx_subscription_payments_status ON subscription_payments(status);
CREATE INDEX IF NOT EXISTS idx_subscription_payments_created_at ON subscription_payments(created_at);
CREATE INDEX IF NOT EXISTS idx_subscription_payments_transaction_id ON subscription_payments(transaction_id);

-- Update users table to include subscription fields if not exists
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'subscription_tier') THEN
        ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(20) DEFAULT 'FREE';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'subscription_expires_at') THEN
        ALTER TABLE users ADD COLUMN subscription_expires_at TIMESTAMP;
    END IF;
END $$;

-- Create usage_tracking table if not exists
CREATE TABLE IF NOT EXISTS usage_tracking (
    id VARCHAR(26) PRIMARY KEY,
    user_id VARCHAR(26) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    action_date DATE NOT NULL,
    count INTEGER DEFAULT 1,
    metadata_json JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for usage_tracking
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_id ON usage_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_action_type ON usage_tracking(action_type);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_action_date ON usage_tracking(action_date);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_action_date ON usage_tracking(user_id, action_type, action_date);

-- Create subscription monitoring views
CREATE OR REPLACE VIEW subscription_metrics AS
SELECT 
    subscription_tier,
    COUNT(*) as user_count,
    COUNT(CASE WHEN subscription_expires_at > NOW() OR subscription_expires_at IS NULL THEN 1 END) as active_count,
    COUNT(CASE WHEN subscription_expires_at <= NOW() THEN 1 END) as expired_count
FROM users 
GROUP BY subscription_tier;

CREATE OR REPLACE VIEW payment_metrics AS
SELECT 
    DATE(created_at) as payment_date,
    subscription_tier,
    status,
    COUNT(*) as payment_count,
    SUM(amount_cents) as total_amount_cents,
    AVG(amount_cents) as avg_amount_cents
FROM subscription_payments 
GROUP BY DATE(created_at), subscription_tier, status
ORDER BY payment_date DESC;

-- Create function to get users with expiring subscriptions
CREATE OR REPLACE FUNCTION get_users_with_expiring_subscriptions(days_ahead INTEGER)
RETURNS TABLE(
    user_id VARCHAR(26),
    email VARCHAR(255),
    subscription_tier VARCHAR(20),
    expires_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email,
        u.subscription_tier,
        u.subscription_expires_at
    FROM users u
    WHERE u.subscription_expires_at IS NOT NULL
    AND u.subscription_expires_at > NOW()
    AND u.subscription_expires_at <= NOW() + INTERVAL '1 day' * days_ahead
    AND u.subscription_tier != 'FREE';
END;
$$ LANGUAGE plpgsql;

-- Create function to get users with expired subscriptions
CREATE OR REPLACE FUNCTION get_users_with_expired_subscriptions()
RETURNS TABLE(
    user_id VARCHAR(26),
    email VARCHAR(255),
    subscription_tier VARCHAR(20),
    expires_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email,
        u.subscription_tier,
        u.subscription_expires_at
    FROM users u
    WHERE u.subscription_expires_at IS NOT NULL
    AND u.subscription_expires_at <= NOW()
    AND u.subscription_tier != 'FREE';
END;
$$ LANGUAGE plpgsql;