import { useState, useEffect, useRef } from 'react';
import { RiRobot2Fill } from 'react-icons/ri';
import { toast } from 'react-toastify';
import { sendMessageToAI, getChatHistory } from '../services/api/chat.service';
import Navbar from '../components/Navbar';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const history = await getChatHistory();
      
      const formattedMessages = history.map((msg, index) => ({
        id: Date.now() + index,
        type: msg.role === 'human' ? 'user' : 'ai',
        text: msg.content,
      }));
      
      setMessages(formattedMessages);
    }  catch (error) {
        if (error.response) {
          toast.error(error.response.data?.detail || 'Signup failed. Please try again.');
        } else if (error.request) {
          toast.error('Network error. Please check your internet connection and try again.');
        } else {
          toast.error('Something went wrong. Please try again.');
        }
    }  finally {
      setIsLoadingHistory(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');

    const newUserMessage = {id: Date.now(),type: 'user',text: userMessage};
    setMessages(prev => [...prev, newUserMessage]);

    // Add thinking placeholder
    const thinkingMessage = {
      id: Date.now() + 1,
      type: 'ai',
      text: 'AI is thinking',
      isThinking: true,
    };
    setMessages(prev => [...prev, thinkingMessage]);

    setIsLoading(true);

    try {
      const response = await sendMessageToAI(userMessage);
      
      const aiResponseText = response.reply || 'No response';

      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.isThinking);
        return [...filtered,
          {
            id: Date.now() + 2,
            type: 'ai',
            text: aiResponseText,
          },
        ];
      });
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Failed to get AI response';
      toast.error(errorMessage);
      
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.isThinking);
        return [
          ...filtered,
          {
            id: Date.now() + 2,
            type: 'ai',
            text: 'Sorry, I encountered an error. Please try again.',
          },
        ];
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <Navbar />

      <div className="chat-messages">
        <div className="messages-container">
          {isLoadingHistory ? (
            <div style={{ textAlign: 'center', padding: '20px', color: '#6b7280' }}>
              Loading chat history...
            </div>
          ) : messages.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '20px', color: '#6b7280' }}>
              What’s on the agenda today?
            </div>
          ) : (
            messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              {message.type === 'ai' ? (
                <div className="message-content">
                  <div className="ai-icon">
                    <RiRobot2Fill />
                  </div>
                  <div className={`message-bubble ${message.isThinking ? 'thinking' : ''}`}>
                    {message.isThinking ? (
                      <>
                        AI is thinking
                        <div className="dots">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </>
                    ) : (
                      message.text
                    )}
                  </div>
                </div>
              ) : (
                <div className="message-bubble">{message.text}</div>
              )}
            </div>
          )))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="chat-input-container">
        <div className="input-wrapper">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button
            className="send-btn"
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
          >

            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
