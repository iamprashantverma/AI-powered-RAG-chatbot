import { useState, useEffect, useRef } from 'react';
import { FiSend, FiX } from 'react-icons/fi';
import { RiRobot2Fill, RiUser3Fill } from 'react-icons/ri';
import { toast } from 'react-toastify';
import { sendMessageToAI, getChatHistory } from '../services/api/chat.service';
import Navbar from '../components/Navbar';
import axios from 'axios';

const Chatbot = () => {
  const controllerRef = useRef(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  useEffect(() => {
    loadChatHistory();
    
    return () => {
      if (controllerRef.current) {
        controllerRef.current.abort();
      }
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [inputValue]);

  const loadChatHistory = async () => {
    try {
      const history = await getChatHistory();
      const formatted = history.map((msg, i) => ({
        id: Date.now() + i,
        type: msg.role === 'human' ? 'user' : 'ai',
        text: msg.content,
      }));
      setMessages(formatted);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const cancelRequest = () => {
    if (controllerRef.current) {
      controllerRef.current.abort();
      controllerRef.current = null;
    }
    setMessages(prev => prev.filter(m => !m.isThinking));
    setIsLoading(false);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() && !isLoading) return;

    if (isLoading) {
      cancelRequest();
      return;
    }

    if (controllerRef.current) {
      controllerRef.current.abort();
    }
    controllerRef.current = new AbortController();

    const userText = inputValue.trim();
    setInputValue('');

    setMessages(prev => [
      ...prev,
      { id: Date.now(), type: 'user', text: userText },
      { id: Date.now() + 1, type: 'ai', text: '', isThinking: true },
    ]);

    setIsLoading(true);

    try {
      const response = await sendMessageToAI(userText, controllerRef.current);
      const aiText = response.reply || response.response || response.message || 'No response';

      setMessages(prev => [
        ...prev.filter(m => !m.isThinking),
        { id: Date.now() + 2, type: 'ai', text: aiText },
      ]);
    } catch (error) {
      if (axios.isCancel(error)|| error?.name === 'CanceledError' || error?.code === 'ERR_CANCELED') {
        setMessages(prev => prev.filter(m => !m.isThinking));
        return;
      }

      toast.error('Failed to get AI response');
      setMessages(prev => [
        ...prev.filter(m => !m.isThinking),
        { id: Date.now(), type: 'ai', text: error?.response?.data?.detail||'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
      controllerRef.current = null;
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <Navbar />

      <div className="chat-messages">
        {isLoadingHistory ? (
          <div className="empty-state">
            <div className="empty-icon">⏳</div>
            <div className="empty-text">Loading your conversations...</div>
          </div>
        ) : messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">💬</div>
            <div className="empty-text">Start a conversation</div>
            <div className="empty-subtext">Ask me anything!</div>
          </div>
        ) : (
          <div className="messages-wrapper">
            {messages.map(msg => (
              <div key={msg.id} className={`message ${msg.type}`}>
                <div className={`avatar ${msg.type}-avatar`}>
                  {msg.type === 'user' ? <RiUser3Fill /> : <RiRobot2Fill />}
                </div>
                <div className="message-content">
                  <div className={`message-bubble ${msg.isThinking ? 'thinking' : ''}`}>
                    {msg.isThinking ? (
                      <>
                        <span className="thinking-text">Thinking</span>
                        <div className="dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </>
                    ) : (
                      msg.text
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <div className="input-container">
          <div className="input-box">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
  
              rows={1}
              maxLength={500}
            />
            <div className="action-buttons">
              {isLoading ? (
                <button className="cancel-btn" onClick={cancelRequest} title="Cancel">
                  <FiX />
                </button>
              ) : (
                <button 
                  className="send-btn" 
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim()}
                  title="Send message"
                >
                  <FiSend />
                </button>
              )}
            </div>
          </div>
          <div className="input-hint">
            <span className="hint-text">
              <span>Press Enter to send, Shift + Enter for new line</span>
            </span>
            <span className="char-count">{inputValue.length} / 500</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
