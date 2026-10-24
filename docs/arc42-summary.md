# arc42 Chapter Summary

A general summary of the twelve arc42 chapters and what each of them should answer. It describes the arc42 template itself, not the BankOCR system. The BankOCR architecture is documented in `docs/architecture/`.

## 1. Introduction and Goals

This chapter explains why the system exists and what matters most. It gives an overview of the requirements, meaning what the system does and its main functions.

It also lists the quality goals. Only the three to five most important ones are chosen, so it does not look like everything has the same priority. The stakeholders are described here as well: everyone who is connected to the system, their role and what they expect from it.

## 2. Constraints

Constraints are requirements that come from outside, from the company, the client or the law. The team does not choose them, but has to respect them.

There are three types: technical constraints (technologies, formats, platforms), organizational constraints (deadlines, budget, team size) and conventions (rules for writing code and documentation, versioning).

## 3. Context and Scope

This chapter sets the boundaries of the system. It shows what belongs to the system, what is outside of it, and how the system is connected to its environment through interfaces.

It has two parts. The Business Context shows who communicates with the system and which data goes in and out. The Technical Context shows how that data travels: protocols, formats and which channel is used for which input.

## 4. Solution Strategy

The solution strategy explains how the problem is solved. It covers the main technology decisions, how the system is divided into parts, and how each quality goal from chapter 1 is achieved.

## 5. Building Block View

This chapter shows which parts the system is made of and how they are connected. It gives a hierarchy of building blocks, from the whole system down to smaller parts, together with the responsibility of each block.

## 6. Runtime View

The runtime view describes how the system behaves while it is running and how its parts work together. It focuses on the most important scenarios, usually shown with sequence diagrams.

## 7. Deployment View

This chapter connects the software with the infrastructure. It shows where and on what the system runs, and which environments exist.

## 8. Cross-cutting Concepts

Some rules and patterns apply to the whole system, not to a single part of it. They are described once in this chapter instead of being repeated in every building block.

## 9. Architecture Decisions

This chapter keeps the reasons behind important decisions. Each decision is recorded with its context, the decision itself, the rationale and the consequences, so that later it is clear why something was done the way it was.

## 10. Quality Requirements

Here the quality goals from chapter 1 become measurable requirements, which are used to check whether the system is good enough.

The chapter contains a quality tree, which groups the requirements into quality categories, and quality scenarios, which describe a context, an event and the expected result.

## 11. Risks and Technical Debts

This is an honest list of the weak points of the architecture. It names the known risks and problems and explains how they can be reduced.

## 12. Glossary

The glossary is the shared language of the team. It contains a table of technical and domain terms, so that everyone uses the same words with the same meaning.
