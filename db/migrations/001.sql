-- Enable uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

---------------------------
-- USERS Table & Policies
---------------------------
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users NOT NULL,
  email TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

---------------------------
-- Trigger to Auto-Create User Entry
---------------------------
CREATE FUNCTION public.handle_new_user() 
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, full_name, avatar_url, email)
  VALUES (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url', new.email);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

---------------------------
-- CALLS Table
---------------------------
CREATE TABLE calls (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
  sid VARCHAR(255) UNIQUE NOT NULL,
  from_number VARCHAR(20) NOT NULL,
  to_number VARCHAR(20) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'INITIALIZED',
  eleven_labs_conversation_id VARCHAR(255),
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- Useful indexes for calls:
CREATE INDEX idx_calls_user_id ON calls(user_id);

---------------------------
-- CHATS Table
---------------------------
CREATE TABLE ai_chats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
  title TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- Index for quick lookup by user
CREATE INDEX idx_ai_chats_user_id ON ai_chats(user_id);

---------------------------
-- MESSAGES Table
---------------------------
CREATE TABLE ai_chat_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chat_id UUID NOT NULL REFERENCES ai_chats(id), 
  user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
  role VARCHAR NOT NULL,
  content JSON NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now()),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc', now())
);

-- Useful indexes for messages:
CREATE INDEX idx_ai_chat_messages_chat_id ON ai_chat_messages(chat_id);
CREATE INDEX idx_ai_chat_messages_chat_id_created_at ON ai_chat_messages(chat_id, created_at);
CREATE INDEX idx_ai_chat_messages_user_id ON ai_chat_messages(user_id);

---------------------------
-- Function & Trigger to Update the updated_at Column
---------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = timezone('utc', now());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the update trigger to all our tables

-- Users table trigger
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Calls table trigger
CREATE TRIGGER update_calls_updated_at
BEFORE UPDATE ON calls
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Ai_chats table trigger
CREATE TRIGGER update_ai_chats_updated_at
BEFORE UPDATE ON ai_chats
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Ai_chat_messages table trigger
CREATE TRIGGER update_ai_chat_messages_updated_at
BEFORE UPDATE ON ai_chat_messages
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
