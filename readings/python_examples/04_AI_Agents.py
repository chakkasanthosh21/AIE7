#!/usr/bin/env python3
"""
🤖 AI Agents Complete Guide
===========================

This file covers AI Agents - autonomous systems that can perceive, think, make 
decisions, and take actions to achieve goals.

What you'll learn:
1. What are AI Agents?
2. Types of AI Agents
3. Building simple agents
4. Multi-agent systems
5. Agent communication and coordination
6. Real-world applications

Author: AI Learning Guide
Date: 2024
"""

import json
import time
import random
import math
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum

# =============================================================================
# SECTION 1: WHAT ARE AI AGENTS?
# =============================================================================

"""
AI Agents are autonomous systems that can:
- Perceive their environment through sensors or data inputs
- Think and reason about what they observe
- Make decisions based on their goals and knowledge
- Take actions to achieve their objectives
- Learn and adapt from experience

Key Characteristics:
- Autonomy: Can operate without constant human intervention
- Reactivity: Respond to changes in their environment
- Proactivity: Take initiative to achieve goals
- Social Ability: Can interact with other agents or humans

Agent Loop:
1. Sense → 2. Think → 3. Act → 4. Learn → (repeat)

Types of Agents:
- Simple Reflex Agents: React based on current perception
- Model-Based Agents: Maintain internal state/model
- Goal-Based Agents: Work toward specific objectives
- Utility-Based Agents: Optimize for maximum utility
- Learning Agents: Improve performance over time
"""

def print_ai_agents_overview():
    """Print an overview of AI Agents"""
    print("🤖 AI Agents Overview")
    print("=" * 30)
    
    concepts = {
        "Definition": "Autonomous systems that perceive, think, decide, and act",
        "Key Characteristic": "Can operate independently to achieve goals",
        "Core Loop": "Sense → Think → Act → Learn",
        "Main Types": "Reflex, Model-Based, Goal-Based, Utility-Based, Learning",
        "Applications": "Chatbots, Game AI, Robotics, Trading Systems, Smart Assistants"
    }
    
    for concept, description in concepts.items():
        print(f"📌 {concept}: {description}")
    
    print("\n💡 Think of AI agents as digital assistants that can work independently!")

# =============================================================================
# SECTION 2: BASIC AGENT FRAMEWORK
# =============================================================================

class AgentState(Enum):
    """Possible states of an agent"""
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    LEARNING = "learning"
    ERROR = "error"

@dataclass
class AgentAction:
    """Represents an action an agent can take"""
    name: str
    parameters: Dict[str, Any]
    confidence: float
    timestamp: float

@dataclass
class AgentObservation:
    """Represents what an agent observes"""
    data: Dict[str, Any]
    timestamp: float
    source: str

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.name = name
        self.capabilities = capabilities
        self.state = AgentState.IDLE
        self.memory = []
        self.performance_metrics = {}
        self.creation_time = time.time()
    
    @abstractmethod
    def perceive(self, environment_data: Dict[str, Any]) -> AgentObservation:
        """Process environment data into observations"""
        pass
    
    @abstractmethod
    def think(self, observation: AgentObservation) -> AgentAction:
        """Process observation and decide on action"""
        pass
    
    @abstractmethod
    def act(self, action: AgentAction) -> Dict[str, Any]:
        """Execute the chosen action"""
        pass
    
    def learn(self, observation: AgentObservation, action: AgentAction, result: Dict[str, Any]):
        """Learn from experience"""
        # Store experience in memory
        experience = {
            "observation": observation,
            "action": action,
            "result": result,
            "timestamp": time.time()
        }
        self.memory.append(experience)
        
        # Keep only recent experiences (last 100)
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def run_cycle(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run one complete agent cycle"""
        try:
            # Step 1: Perceive
            self.state = AgentState.THINKING
            observation = self.perceive(environment_data)
            
            # Step 2: Think
            action = self.think(observation)
            
            # Step 3: Act
            self.state = AgentState.ACTING
            result = self.act(action)
            
            # Step 4: Learn
            self.state = AgentState.LEARNING
            self.learn(observation, action, result)
            
            # Return to idle
            self.state = AgentState.IDLE
            
            return {
                "observation": observation,
                "action": action,
                "result": result,
                "success": True
            }
            
        except Exception as e:
            self.state = AgentState.ERROR
            return {
                "error": str(e),
                "success": False
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "capabilities": self.capabilities,
            "memory_size": len(self.memory),
            "uptime": time.time() - self.creation_time
        }

# =============================================================================
# SECTION 3: SIMPLE REFLEX AGENT
# =============================================================================

class SimpleReflexAgent(BaseAgent):
    """A simple reflex agent that reacts based on current input"""
    
    def __init__(self, name: str, rules: Dict[str, str]):
        super().__init__(name, ["reflex_response"])
        self.rules = rules  # condition -> action mapping
    
    def perceive(self, environment_data: Dict[str, Any]) -> AgentObservation:
        """Extract relevant information from environment"""
        return AgentObservation(
            data=environment_data,
            timestamp=time.time(),
            source="environment"
        )
    
    def think(self, observation: AgentObservation) -> AgentAction:
        """Apply simple rules to determine action"""
        # Check each rule against current observation
        for condition, action in self.rules.items():
            if self._condition_matches(condition, observation.data):
                return AgentAction(
                    name=action,
                    parameters={},
                    confidence=1.0,
                    timestamp=time.time()
                )
        
        # Default action if no rules match
        return AgentAction(
            name="no_action",
            parameters={},
            confidence=0.0,
            timestamp=time.time()
        )
    
    def act(self, action: AgentAction) -> Dict[str, Any]:
        """Execute the action"""
        if action.name == "no_action":
            return {"message": "No action taken"}
        
        return {
            "action_executed": action.name,
            "message": f"Executed {action.name}",
            "timestamp": action.timestamp
        }
    
    def _condition_matches(self, condition: str, data: Dict[str, Any]) -> bool:
        """Check if a condition matches the current data"""
        # Simple string matching - in practice, you'd use more sophisticated logic
        return condition.lower() in str(data).lower()

def demonstrate_simple_reflex_agent():
    """Demonstrate a simple reflex agent"""
    print("\n🔄 Simple Reflex Agent")
    print("=" * 25)
    
    # Create rules for a simple chatbot agent
    rules = {
        "hello": "greet",
        "how are you": "respond_wellbeing",
        "weather": "check_weather",
        "time": "tell_time",
        "help": "provide_help"
    }
    
    # Create the agent
    agent = SimpleReflexAgent("ChatBot", rules)
    
    # Test the agent with different inputs
    test_inputs = [
        {"message": "Hello there!"},
        {"message": "How are you doing?"},
        {"message": "What's the weather like?"},
        {"message": "What time is it?"},
        {"message": "I need help"},
        {"message": "Random message"}
    ]
    
    print("\n🤖 Testing Simple Reflex Agent:")
    print("-" * 35)
    
    for input_data in test_inputs:
        print(f"\nInput: {input_data}")
        result = agent.run_cycle(input_data)
        
        if result["success"]:
            print(f"Action: {result['action'].name}")
            print(f"Response: {result['result']['message']}")
        else:
            print(f"Error: {result['error']}")
    
    # Show agent status
    print(f"\n📊 Agent Status:")
    status = agent.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    return agent

# =============================================================================
# SECTION 4: GOAL-BASED AGENT
# =============================================================================

@dataclass
class Goal:
    """Represents a goal for an agent"""
    name: str
    description: str
    priority: int  # 1 = highest priority
    completed: bool = False

class GoalBasedAgent(BaseAgent):
    """An agent that works toward specific goals"""
    
    def __init__(self, name: str, goals: List[Goal]):
        super().__init__(name, ["goal_planning", "action_execution"])
        self.goals = goals
        self.current_goal = None
        self.plan = []
    
    def perceive(self, environment_data: Dict[str, Any]) -> AgentObservation:
        """Process environment data and check goal progress"""
        # Check if current goal is completed
        if self.current_goal:
            if self._is_goal_completed(environment_data):
                self.current_goal.completed = True
                self.current_goal = None
                self.plan = []
        
        return AgentObservation(
            data=environment_data,
            timestamp=time.time(),
            source="environment"
        )
    
    def think(self, observation: AgentObservation) -> AgentAction:
        """Plan actions to achieve current goal"""
        # Select new goal if none is active
        if not self.current_goal:
            self.current_goal = self._select_next_goal()
            if self.current_goal:
                self.plan = self._create_plan(self.current_goal, observation.data)
        
        # Execute next action in plan
        if self.plan:
            next_action = self.plan.pop(0)
            return AgentAction(
                name=next_action["name"],
                parameters=next_action.get("parameters", {}),
                confidence=0.8,
                timestamp=time.time()
            )
        
        return AgentAction(
            name="no_action",
            parameters={},
            confidence=0.0,
            timestamp=time.time()
        )
    
    def act(self, action: AgentAction) -> Dict[str, Any]:
        """Execute the action"""
        if action.name == "no_action":
            return {"message": "No action to take"}
        
        # Simulate action execution
        result = {
            "action_executed": action.name,
            "goal": self.current_goal.name if self.current_goal else "None",
            "message": f"Executed {action.name} for goal: {self.current_goal.name if self.current_goal else 'None'}"
        }
        
        return result
    
    def _select_next_goal(self) -> Optional[Goal]:
        """Select the next goal to work on"""
        incomplete_goals = [goal for goal in self.goals if not goal.completed]
        if incomplete_goals:
            # Select goal with highest priority (lowest number)
            return min(incomplete_goals, key=lambda g: g.priority)
        return None
    
    def _create_plan(self, goal: Goal, environment_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a plan to achieve the goal"""
        # Simple planning - in practice, you'd use more sophisticated planning algorithms
        plans = {
            "collect_data": [
                {"name": "scan_environment", "parameters": {}},
                {"name": "gather_information", "parameters": {}}
            ],
            "analyze_data": [
                {"name": "process_data", "parameters": {}},
                {"name": "identify_patterns", "parameters": {}}
            ],
            "generate_report": [
                {"name": "compile_findings", "parameters": {}},
                {"name": "create_report", "parameters": {}}
            ]
        }
        
        return plans.get(goal.name, [{"name": "work_on_goal", "parameters": {"goal": goal.name}}])
    
    def _is_goal_completed(self, environment_data: Dict[str, Any]) -> bool:
        """Check if current goal is completed"""
        # Simple completion check - in practice, you'd have more sophisticated logic
        return random.random() < 0.3  # 30% chance of completion for demonstration

def demonstrate_goal_based_agent():
    """Demonstrate a goal-based agent"""
    print("\n🎯 Goal-Based Agent")
    print("=" * 25)
    
    # Create goals
    goals = [
        Goal("collect_data", "Collect relevant data from environment", 1),
        Goal("analyze_data", "Analyze collected data for insights", 2),
        Goal("generate_report", "Generate a comprehensive report", 3)
    ]
    
    # Create the agent
    agent = GoalBasedAgent("DataAnalyst", goals)
    
    # Test the agent
    print("\n🤖 Testing Goal-Based Agent:")
    print("-" * 30)
    
    for cycle in range(10):
        print(f"\n--- Cycle {cycle + 1} ---")
        
        # Simulate environment data
        environment_data = {
            "data_available": random.choice([True, False]),
            "analysis_needed": random.choice([True, False]),
            "report_requested": random.choice([True, False])
        }
        
        result = agent.run_cycle(environment_data)
        
        if result["success"]:
            print(f"Action: {result['action'].name}")
            print(f"Goal: {result['result']['goal']}")
            print(f"Message: {result['result']['message']}")
        else:
            print(f"Error: {result['error']}")
        
        # Show current status
        status = agent.get_status()
        print(f"Active Goals: {len([g for g in goals if not g.completed])}")
    
    # Show final status
    print(f"\n📊 Final Status:")
    for goal in goals:
        print(f"  {goal.name}: {'✅ Completed' if goal.completed else '⏳ Pending'}")
    
    return agent

# =============================================================================
# SECTION 5: LEARNING AGENT
# =============================================================================

@dataclass
class LearningExperience:
    """Represents a learning experience"""
    state: Dict[str, Any]
    action: str
    reward: float
    next_state: Dict[str, Any]
    timestamp: float

class LearningAgent(BaseAgent):
    """An agent that learns from experience"""
    
    def __init__(self, name: str, learning_rate: float = 0.1):
        super().__init__(name, ["learning", "adaptation"])
        self.learning_rate = learning_rate
        self.q_table = {}  # Simple Q-learning table
        self.experiences = []
        self.epsilon = 0.1  # Exploration rate
    
    def perceive(self, environment_data: Dict[str, Any]) -> AgentObservation:
        """Process environment data"""
        return AgentObservation(
            data=environment_data,
            timestamp=time.time(),
            source="environment"
        )
    
    def think(self, observation: AgentObservation) -> AgentAction:
        """Choose action using learned policy"""
        state_key = self._get_state_key(observation.data)
        
        # Initialize Q-values for new state
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        
        # Choose action (epsilon-greedy)
        if random.random() < self.epsilon:
            # Exploration: random action
            action = random.choice(self._get_available_actions())
        else:
            # Exploitation: best known action
            action = self._get_best_action(state_key)
        
        return AgentAction(
            name=action,
            parameters={},
            confidence=self._get_action_confidence(state_key, action),
            timestamp=time.time()
        )
    
    def act(self, action: AgentAction) -> Dict[str, Any]:
        """Execute action and get reward"""
        # Simulate action execution and reward
        reward = self._calculate_reward(action.name)
        
        return {
            "action_executed": action.name,
            "reward": reward,
            "message": f"Executed {action.name}, received reward: {reward}"
        }
    
    def learn(self, observation: AgentObservation, action: AgentAction, result: Dict[str, Any]):
        """Learn from experience using Q-learning"""
        # Store experience
        experience = LearningExperience(
            state=observation.data,
            action=action.name,
            reward=result["reward"],
            next_state=observation.data,  # Simplified - in practice, this would be the next state
            timestamp=time.time()
        )
        self.experiences.append(experience)
        
        # Update Q-values
        self._update_q_values(experience)
        
        # Reduce exploration over time
        self.epsilon = max(0.01, self.epsilon * 0.995)
    
    def _get_state_key(self, state: Dict[str, Any]) -> str:
        """Convert state to string key"""
        return str(sorted(state.items()))
    
    def _get_available_actions(self) -> List[str]:
        """Get list of available actions"""
        return ["action_a", "action_b", "action_c", "action_d"]
    
    def _get_best_action(self, state_key: str) -> str:
        """Get the best action for a given state"""
        if state_key not in self.q_table or not self.q_table[state_key]:
            return random.choice(self._get_available_actions())
        
        return max(self.q_table[state_key].items(), key=lambda x: x[1])[0]
    
    def _get_action_confidence(self, state_key: str, action: str) -> float:
        """Get confidence in an action"""
        if state_key in self.q_table and action in self.q_table[state_key]:
            return min(1.0, abs(self.q_table[state_key][action]) / 10.0)
        return 0.1
    
    def _calculate_reward(self, action: str) -> float:
        """Calculate reward for an action"""
        # Simple reward function - in practice, this would be based on environment
        rewards = {
            "action_a": 2.0,
            "action_b": 1.0,
            "action_c": 3.0,
            "action_d": 0.5
        }
        return rewards.get(action, 0.0) + random.uniform(-0.5, 0.5)
    
    def _update_q_values(self, experience: LearningExperience):
        """Update Q-values using Q-learning"""
        state_key = self._get_state_key(experience.state)
        next_state_key = self._get_state_key(experience.next_state)
        
        # Initialize Q-values if needed
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {}
        
        # Get current Q-value
        current_q = self.q_table[state_key].get(experience.action, 0.0)
        
        # Get max Q-value for next state
        max_next_q = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0.0
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (experience.reward + 0.9 * max_next_q - current_q)
        self.q_table[state_key][experience.action] = new_q

def demonstrate_learning_agent():
    """Demonstrate a learning agent"""
    print("\n🧠 Learning Agent")
    print("=" * 20)
    
    # Create learning agent
    agent = LearningAgent("Learner", learning_rate=0.1)
    
    # Test the agent over multiple cycles
    print("\n🤖 Testing Learning Agent:")
    print("-" * 25)
    
    total_reward = 0
    for cycle in range(20):
        # Simulate environment
        environment_data = {
            "situation": random.choice(["normal", "challenging", "easy"]),
            "resources": random.randint(1, 10)
        }
        
        result = agent.run_cycle(environment_data)
        
        if result["success"]:
            reward = result["result"]["reward"]
            total_reward += reward
            print(f"Cycle {cycle + 1}: Action={result['action'].name}, Reward={reward:.2f}, Confidence={result['action'].confidence:.2f}")
        else:
            print(f"Cycle {cycle + 1}: Error - {result['error']}")
    
    # Show learning results
    print(f"\n📊 Learning Results:")
    print(f"Total Reward: {total_reward:.2f}")
    print(f"Average Reward: {total_reward / 20:.2f}")
    print(f"Q-table size: {len(agent.q_table)}")
    print(f"Final exploration rate: {agent.epsilon:.3f}")
    
    # Show some learned Q-values
    print(f"\n🎓 Learned Q-values (sample):")
    for i, (state_key, actions) in enumerate(list(agent.q_table.items())[:3]):
        print(f"  State {i}: {dict(actions)}")
    
    return agent

# =============================================================================
# SECTION 6: MULTI-AGENT SYSTEM
# =============================================================================

@dataclass
class Message:
    """Represents a message between agents"""
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str
    timestamp: float

class MultiAgentSystem:
    """A system that coordinates multiple agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[Message] = []
        self.coordination_rules: Dict[str, Callable] = {}
    
    def add_agent(self, agent: BaseAgent):
        """Add an agent to the system"""
        self.agents[agent.name] = agent
    
    def send_message(self, message: Message):
        """Send a message between agents"""
        self.message_queue.append(message)
    
    def broadcast_message(self, sender: str, content: Dict[str, Any], message_type: str = "info"):
        """Broadcast message to all agents"""
        for agent_name in self.agents:
            if agent_name != sender:
                message = Message(
                    sender=sender,
                    receiver=agent_name,
                    content=content,
                    message_type=message_type,
                    timestamp=time.time()
                )
                self.send_message(message)
    
    def process_messages(self):
        """Process all pending messages"""
        processed_messages = []
        
        for message in self.message_queue:
            if message.receiver in self.agents:
                # Deliver message to agent
                agent = self.agents[message.receiver]
                if hasattr(agent, 'receive_message'):
                    agent.receive_message(message)
                processed_messages.append(message)
        
        # Remove processed messages
        for message in processed_messages:
            self.message_queue.remove(message)
    
    def run_cycle(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run one cycle of the multi-agent system"""
        results = {}
        
        # Process messages
        self.process_messages()
        
        # Run each agent
        for agent_name, agent in self.agents.items():
            result = agent.run_cycle(environment_data)
            results[agent_name] = result
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of the entire system"""
        return {
            "system_name": self.name,
            "agent_count": len(self.agents),
            "pending_messages": len(self.message_queue),
            "agents": {name: agent.get_status() for name, agent in self.agents.items()}
        }

class CollaborativeAgent(BaseAgent):
    """An agent that can collaborate with others"""
    
    def __init__(self, name: str, role: str):
        super().__init__(name, ["collaboration", "communication"])
        self.role = role
        self.received_messages = []
        self.collaboration_partners = []
    
    def receive_message(self, message: Message):
        """Receive a message from another agent"""
        self.received_messages.append(message)
        
        # Keep only recent messages
        if len(self.received_messages) > 50:
            self.received_messages = self.received_messages[-50:]
    
    def perceive(self, environment_data: Dict[str, Any]) -> AgentObservation:
        """Process environment data and messages"""
        # Combine environment data with received messages
        combined_data = {
            "environment": environment_data,
            "messages": [msg.content for msg in self.received_messages[-5:]]  # Last 5 messages
        }
        
        return AgentObservation(
            data=combined_data,
            timestamp=time.time(),
            source="environment_and_messages"
        )
    
    def think(self, observation: AgentObservation) -> AgentAction:
        """Decide on action based on role and messages"""
        # Simple role-based decision making
        if self.role == "coordinator":
            action_name = "coordinate_team"
        elif self.role == "worker":
            action_name = "perform_task"
        elif self.role == "monitor":
            action_name = "check_status"
        else:
            action_name = "default_action"
        
        return AgentAction(
            name=action_name,
            parameters={"role": self.role},
            confidence=0.8,
            timestamp=time.time()
        )
    
    def act(self, action: AgentAction) -> Dict[str, Any]:
        """Execute action and potentially send messages"""
        result = {
            "action_executed": action.name,
            "role": action.parameters.get("role", "unknown"),
            "message": f"{self.name} ({self.role}) executed {action.name}"
        }
        
        # Send status message to other agents
        status_message = {
            "agent": self.name,
            "action": action.name,
            "status": "completed"
        }
        
        return result

def demonstrate_multi_agent_system():
    """Demonstrate a multi-agent system"""
    print("\n👥 Multi-Agent System")
    print("=" * 25)
    
    # Create multi-agent system
    mas = MultiAgentSystem("ProjectTeam")
    
    # Create different types of agents
    coordinator = CollaborativeAgent("Coordinator", "coordinator")
    worker1 = CollaborativeAgent("Worker1", "worker")
    worker2 = CollaborativeAgent("Worker2", "worker")
    monitor = CollaborativeAgent("Monitor", "monitor")
    
    # Add agents to system
    mas.add_agent(coordinator)
    mas.add_agent(worker1)
    mas.add_agent(worker2)
    mas.add_agent(monitor)
    
    # Test the system
    print("\n🤖 Testing Multi-Agent System:")
    print("-" * 35)
    
    for cycle in range(5):
        print(f"\n--- Cycle {cycle + 1} ---")
        
        # Simulate environment
        environment_data = {
            "project_status": random.choice(["planning", "execution", "review"]),
            "team_health": random.randint(1, 10),
            "deadline_pressure": random.choice(["low", "medium", "high"])
        }
        
        # Run system cycle
        results = mas.run_cycle(environment_data)
        
        # Display results
        for agent_name, result in results.items():
            if result["success"]:
                print(f"  {agent_name}: {result['result']['message']}")
            else:
                print(f"  {agent_name}: Error - {result['error']}")
    
    # Show system status
    print(f"\n📊 System Status:")
    status = mas.get_system_status()
    print(f"  Agents: {status['agent_count']}")
    print(f"  Pending Messages: {status['pending_messages']}")
    
    for agent_name, agent_status in status['agents'].items():
        print(f"  {agent_name}: {agent_status['state']}")
    
    return mas

# =============================================================================
# SECTION 7: REAL-WORLD AGENT APPLICATIONS
# =============================================================================

def demonstrate_real_world_applications():
    """Demonstrate real-world agent applications"""
    print("\n🌍 Real-World Agent Applications")
    print("=" * 35)
    
    applications = [
        {
            "name": "Trading Agents",
            "description": "Automated trading systems that make buy/sell decisions",
            "agent_type": "Goal-Based + Learning",
            "capabilities": ["Market analysis", "Risk assessment", "Portfolio optimization"],
            "benefits": ["24/7 trading", "Emotion-free decisions", "Fast execution"]
        },
        {
            "name": "Game AI",
            "description": "AI characters in video games with realistic behavior",
            "agent_type": "Goal-Based + Learning",
            "capabilities": ["Pathfinding", "Combat tactics", "Social interaction"],
            "benefits": ["Immersive gameplay", "Adaptive difficulty", "Realistic NPCs"]
        },
        {
            "name": "Smart Home Agents",
            "description": "Automated home management systems",
            "agent_type": "Reflex + Goal-Based",
            "capabilities": ["Climate control", "Security monitoring", "Energy optimization"],
            "benefits": ["Energy savings", "Convenience", "Security"]
        },
        {
            "name": "Customer Service Bots",
            "description": "AI assistants that handle customer inquiries",
            "agent_type": "Reflex + Learning",
            "capabilities": ["Question answering", "Ticket routing", "Sentiment analysis"],
            "benefits": ["24/7 availability", "Scalability", "Consistent service"]
        },
        {
            "name": "Autonomous Vehicles",
            "description": "Self-driving cars that navigate safely",
            "agent_type": "Multi-Agent + Learning",
            "capabilities": ["Path planning", "Obstacle avoidance", "Traffic prediction"],
            "benefits": ["Safety", "Efficiency", "Accessibility"]
        }
    ]
    
    for i, app in enumerate(applications, 1):
        print(f"\n{i}. {app['name']}:")
        print(f"   Description: {app['description']}")
        print(f"   Agent Type: {app['agent_type']}")
        print(f"   Capabilities: {', '.join(app['capabilities'])}")
        print(f"   Benefits: {', '.join(app['benefits'])}")
        print("-" * 50)

# =============================================================================
# SECTION 8: AGENT DEVELOPMENT FRAMEWORK
# =============================================================================

class AgentBuilder:
    """Helper class to build custom agents"""
    
    def __init__(self):
        self.agents = {}
        self.multi_agent_systems = {}
    
    def create_reflex_agent(self, name: str, rules: Dict[str, str]) -> SimpleReflexAgent:
        """Create a simple reflex agent"""
        agent = SimpleReflexAgent(name, rules)
        self.agents[name] = agent
        return agent
    
    def create_goal_agent(self, name: str, goals: List[Goal]) -> GoalBasedAgent:
        """Create a goal-based agent"""
        agent = GoalBasedAgent(name, goals)
        self.agents[name] = agent
        return agent
    
    def create_learning_agent(self, name: str, learning_rate: float = 0.1) -> LearningAgent:
        """Create a learning agent"""
        agent = LearningAgent(name, learning_rate)
        self.agents[name] = agent
        return agent
    
    def create_collaborative_agent(self, name: str, role: str) -> CollaborativeAgent:
        """Create a collaborative agent"""
        agent = CollaborativeAgent(name, role)
        self.agents[name] = agent
        return agent
    
    def create_multi_agent_system(self, name: str, agent_names: List[str]) -> MultiAgentSystem:
        """Create a multi-agent system with specified agents"""
        mas = MultiAgentSystem(name)
        
        for agent_name in agent_names:
            if agent_name in self.agents:
                mas.add_agent(self.agents[agent_name])
        
        self.multi_agent_systems[name] = mas
        return mas
    
    def test_agent(self, agent_name: str, test_cycles: int = 5):
        """Test a specific agent"""
        if agent_name not in self.agents:
            print(f"Agent '{agent_name}' not found!")
            return
        
        agent = self.agents[agent_name]
        print(f"\n🧪 Testing Agent: {agent_name}")
        print("-" * 30)
        
        for cycle in range(test_cycles):
            environment_data = {
                "cycle": cycle,
                "random_data": random.randint(1, 100),
                "timestamp": time.time()
            }
            
            result = agent.run_cycle(environment_data)
            
            if result["success"]:
                print(f"Cycle {cycle + 1}: {result['action'].name} - {result['result']['message']}")
            else:
                print(f"Cycle {cycle + 1}: Error - {result['error']}")
    
    def test_multi_agent_system(self, system_name: str, test_cycles: int = 3):
        """Test a multi-agent system"""
        if system_name not in self.multi_agent_systems:
            print(f"Multi-agent system '{system_name}' not found!")
            return
        
        mas = self.multi_agent_systems[system_name]
        print(f"\n🧪 Testing Multi-Agent System: {system_name}")
        print("-" * 40)
        
        for cycle in range(test_cycles):
            print(f"\n--- Cycle {cycle + 1} ---")
            
            environment_data = {
                "cycle": cycle,
                "system_load": random.randint(1, 10),
                "coordination_needed": random.choice([True, False])
            }
            
            results = mas.run_cycle(environment_data)
            
            for agent_name, result in results.items():
                if result["success"]:
                    print(f"  {agent_name}: {result['result']['message']}")
                else:
                    print(f"  {agent_name}: Error - {result['error']}")

def demonstrate_agent_builder():
    """Demonstrate the agent builder framework"""
    print("\n🔨 Agent Development Framework")
    print("=" * 35)
    
    # Create agent builder
    builder = AgentBuilder()
    
    # Create different types of agents
    reflex_agent = builder.create_reflex_agent("Helper", {
        "help": "provide_assistance",
        "question": "answer_question",
        "problem": "solve_problem"
    })
    
    goals = [
        Goal("analyze_data", "Analyze incoming data", 1),
        Goal("generate_insights", "Generate insights from analysis", 2)
    ]
    goal_agent = builder.create_goal_agent("Analyst", goals)
    
    learning_agent = builder.create_learning_agent("Learner", learning_rate=0.15)
    
    collaborative_agent = builder.create_collaborative_agent("Coordinator", "team_lead")
    
    # Create multi-agent system
    mas = builder.create_multi_agent_system("DataTeam", ["Helper", "Analyst", "Learner", "Coordinator"])
    
    # Test individual agents
    builder.test_agent("Helper", test_cycles=3)
    builder.test_agent("Analyst", test_cycles=3)
    builder.test_agent("Learner", test_cycles=3)
    
    # Test multi-agent system
    builder.test_multi_agent_system("DataTeam", test_cycles=2)
    
    return builder

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run all AI agent demonstrations"""
    print("🤖 AI Agents Complete Guide")
    print("=" * 40)
    print("This file contains comprehensive examples and explanations for AI Agents.")
    print("Run individual functions to explore different concepts.\n")
    
    # Run all demonstrations
    print_ai_agents_overview()
    demonstrate_simple_reflex_agent()
    demonstrate_goal_based_agent()
    demonstrate_learning_agent()
    demonstrate_multi_agent_system()
    demonstrate_real_world_applications()
    demonstrate_agent_builder()
    
    print("\n🎉 Congratulations! You've completed the AI Agents section!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Practice building different types of agents")
    print("2. Experiment with multi-agent coordination")
    print("3. Implement learning algorithms")
    print("4. Build agents for specific applications")
    print("5. Explore the other Python files in this folder")
    
    print("\n💡 To build your own agents, use the AgentBuilder class!")

if __name__ == "__main__":
    main() 