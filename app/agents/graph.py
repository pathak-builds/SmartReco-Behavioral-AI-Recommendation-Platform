"""
LangGraph recommendation workflow.
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END
from langgraph.graph import StateGraph

from app.agents.behavior_analyst import BehaviorAnalyst
from app.agents.memory_agent import MemoryAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.strategist import RecommendationStrategist
from app.agents.persuasion import PersuasionAgent


# ==========================================================
# State
# ==========================================================

class RecommendationState(TypedDict):

    events: list

    analysis: dict

    profile: dict

    retrieved: list

    ranked: list

    recommendations: list
    
class RecommendationGraph:

    def __init__(self):

        self.behavior = BehaviorAnalyst()

        self.memory = MemoryAgent()

        self.retrieval = RetrievalAgent()

        self.strategist = RecommendationStrategist()

        self.persuasion = PersuasionAgent()
        
    def analyze_behavior(
        self,
        state: RecommendationState,
    ):

        state["analysis"] = self.behavior.analyze(
            state["events"]
        )

        return state
    
    def build_profile(
        self,
        state: RecommendationState,
    ):

        state["profile"] = self.memory.build_profile(

            state["analysis"]

        )

        return state
    
    def retrieve(
        self,
        state: RecommendationState,
    ):

        state["retrieved"] = self.retrieval.retrieve(

            state["profile"]

        )

        return state
    
    def rank(
        self,
        state: RecommendationState,
    ):

        state["ranked"] = self.strategist.rank(

            state["retrieved"],

            state["profile"]

        )

        return state
    
    def explain(
        self,
        state: RecommendationState,
    ):

        recommendations = []

        for product in state["ranked"]:

            recommendations.append(

                self.persuasion.build_recommendation(

                    product,

                    state["profile"]

                )

            )

        state["recommendations"] = recommendations

        return state
    
    def compile(self):

        workflow = StateGraph(

            RecommendationState

        )

        workflow.add_node(

            "behavior",

            self.analyze_behavior

        )

        workflow.add_node(

            "memory",

            self.build_profile

        )

        workflow.add_node(

            "retrieval",

            self.retrieve

        )

        workflow.add_node(

            "ranking",

            self.rank

        )

        workflow.add_node(

            "persuasion",

            self.explain

        )

        workflow.set_entry_point(

            "behavior"

        )

        workflow.add_edge(

            "behavior",

            "memory"

        )

        workflow.add_edge(

            "memory",

            "retrieval"

        )

        workflow.add_edge(

            "retrieval",

            "ranking"

        )

        workflow.add_edge(

            "ranking",

            "persuasion"

        )

        workflow.add_edge(

            "persuasion",

            END

        )

        return workflow.compile()