# Concept — The Mechanism of R38ET

*A framework of principles, not a blueprint*

## What this document is

PHILOSOPHY.md states why R38ET exists. MANIFESTO.md states it in public, briefly. This document sits between them: it describes the mechanism — the rules that make the framework act, and act identically, on every level.

R38ET is a framework whose rules and mechanics read and act the same on every level. That sameness is the whole design. A rule that holds in a neighbourhood plenum and a rule that holds in a world assembly are the same rule, applied to a different set of members.

For that reason the framework deliberately does not found itself on nations, continents, or fixed member counts. Those are descriptions of the world as it is today. A constitution that names today's states as its building blocks is wrong within decades — not because the states are bad, but because they are contingent. Borders move, unions form and dissolve, populations grow and shrink, and names change. A framework that treated any of this as structure would need to be rewritten by the very generation it is meant to serve, and every rewriting of a constitution reopens the questions the constitution was supposed to settle.

What is fixed are principles. What varies are the numbers a given generation writes into them: the size of a plenum, the width of an address space, the number of levels that follows from both. This document states the principles and, where a number is unavoidable, marks it as an example.

## The founding principle: one person, one voice

One person, one voice. This is the axiom of the whole design, and it holds on every level without exception. No council, committee, office or function carries more weight than a person. A delegate does not speak with a louder voice than the person who mandated them; they speak with that person's voice, and no other.

The axiom has a consequence that is often overlooked: it turns identity into the load-bearing element of the entire structure. If one person really is one voice, then the question "who is a person here" is not an administrative detail but the attack surface of the cascade. A single forged neighbourhood node is a forged delegate on every level above it. The falsification does not need to reach the world assembly to act there; it only needs to sit at the bottom and be counted upward.

This is why the Web of Trust and sybil resistance matter to the framework, and why they matter structurally rather than as security features bolted on afterwards. The Web of Trust must do two things, and the second is the harder one:

- It must reject sybils — entities that claim to be persons in order to be counted twice or many times.
- It must make the delegation chain verifiable end to end, so that any participant can trace a delegate at level 8 back through the councils that mandated them to the persons who mandated them.

A Web of Trust that only filters at entry leaves the middle of the chain unverified, and a chain verified only at its ends is not verified. The framework's claim to legitimacy rests on the chain being checkable at every link.

## Three rules of constitution

These three rules are the core of the mechanism. They are stated as principles, not as procedures; a generation applying them will write procedures, and those procedures will differ between contexts.

**1. A council comes into being by accession, not by decree.**

When two people meet where no council yet exists, a level-1 plenum is founded. That meeting is the trigger, not a licence: each further person joins that plenum rather than opening their own. The same mechanism continues upward. A council comes into being when at least two councils of the level below accede to it. No council exists without members, and nobody can proclaim a council that nobody joins.

This is the rule that makes the framework federal in the strict sense. It also removes a class of failure that is otherwise hard to prevent: a body that declares itself and then seeks legitimacy. Under accession, a body without acceding members is not a small council or a weak council — it is not a council.

**2. From 16 members, a council may elect delegates. Below that it is a plenum deciding directly.**

A plenum below that size does not delegate; it decides. Delegates are bound by imperative mandate and are recallable at any time — a delegate carries instructions and can be replaced when those instructions are no longer carried.

The threshold of 16 is a principle about scale, not a magic number. It marks the point where direct assembly stops being practical: a group small enough to decide together should decide together, because delegation there costs more than it saves. Where exactly that point lies is a judgement a generation makes; that such a point exists is the principle.

**3. From level 2 upward, councils may decide that a committee is necessary.**

Committees are the executive. They have no cascade of their own: their tasks and spheres of action are decided by the councils that establish them. A committee on one level is not a smaller copy of a committee on another level, and committee structure does not mirror council structure.

The reason is arithmetic and practical at once. A city with hundreds of neighbourhoods needs a handful of committees — building, education and research, economy, and so on — not one committee per neighbourhood. The executive is a cross-section of the work a level actually has to do; it is not a fractal of the legislative cascade. Because committees are established by decision rather than by accession, they can also be shaped to the task instead of to the geography.

## Two cascades

The mechanism runs in two directions, and both are needed.

**Top-down: Lex Superior.** Subordinate norms must satisfy the invariants of the higher level. No norm on a lower level may contradict a norm on a higher one, and the invariants — human rights, the ecological ceiling — are not negotiable downward. This is the layer that keeps a cascade from becoming a set of unrelated assemblies.

**Bottom-up: subsidiarity, Lex Specialis.** Rules are ratified at the lowest level that can carry them. The next higher council decides whether to adopt a norm upward; it does not pre-empt the lower level's competence. What a level does not expressly claim falls downward, by default, to the level that can act.

The consequence that matters most is quantitative. The number of decisions decreases as the level rises. A neighbourhood plenum decides many things; a city council decides fewer; a world assembly decides very few. A global council does not decide whether a school is built. It decides whether education is an inalienable human right. It does not decide a budget; it decides the invariants a budget must satisfy.

This is what makes a proportional world council unthreatening, and it is worth stating plainly because the opposite is usually assumed. The fear attached to world government is the fear of a body that decides everything. A body that decides a handful of questions a year — and whose decisions are the invariants that lower levels must already satisfy — is not that body. The reduction in decision count is not a side effect of the design. It is the design.

## The role of the NormLinter

The NormLinter is strictly an assisting tool. It checks the deontological logic of a norm and flags a violation, failing closed — that is, in doubt it reports the doubt rather than passing the norm. It never decides.

Decisions are made by people only. If a council overrides a flagged violation, the override is recorded as such, with the flag still attached to the norm and visible to everyone downstream. The record is the accountability; the tool is not the authority.

This must be stated plainly and without hedging, because the alternative is the opposite of the framework. An automatic block would be a decision made by a system that no one elected and that no one can recall — exactly the technocratic enclosure the framework opposes. A linter that could refuse a norm would be an upper chamber of one.

## The address space

Councils and committees together must fit into an address space. Today that is 29 bits for councils and committees, against 33 bits for humanity — about 8.59 billion people.

These are parameters, not constants. A generation with a different population writes different numbers: 30 or 34 bits as the population grows toward roughly 10 billion, and 2^34 would leave room far beyond the expected maximum. The principles do not change when the numbers do. What a generation owes the next is not the correct number but the correct relationship between the numbers.

That relationship, in one sentence: the number of councils on all levels together must fit into the address space, and the branching must be chosen so that exactly one council remains at the top. The first condition is about capacity — there must be room for every council and committee the population produces. The second is about shape — the cascade must close at the top instead of fanning out.

A worked example, not a construction manual: with 8 levels, plena of 16 people and a branching factor of 16, both conditions hold. That is why 8 levels is not an arbitrary choice but a consequence. The eight is derived, not decreed; a different branching factor or a different plenum size would yield a different number of levels, and that would be equally correct if both conditions still held. A generation that changes the population figure has to repeat the check. The check is arithmetic and belongs to whoever writes the parameters.

## The eight levels (a possible instantiation)

What follows is one possible instantiation of the framework — the matrix as it stands in MANIFESTO.md. It is an example of the mechanism applied to the world as it currently is, not the structure of the mechanism itself.

| Level | Legislative Board | Executive Committee | Norm Hierarchy |
| :---: | :--- | :--- | :--- |
| 8 | Global Assembly | Planetary Committee | Basic Human Rights |
| 7 | Continental Council | Peace / Continental Coordination | Continental Accords |
| 6 | Federal Parliament | Justice & Social Equity | Federal Law |
| 5 | State Senate | Transportation & Networks | State Acts |
| 4 | Regional Congress | Production & Infrastructure | Regional Statutes |
| 3 | City Council | Housing, Health, Education Services | City Codes |
| 2 | District Bureau | Resource Distribution Workgroups | District Directives |
| 1 | Neighborhood Board | Political Voice | Local Agreements |

A note on the names. "Continental", "federal" and "state" are inherited from the world as it is; the framework does not require them. A different world would fill the same eight rows differently — with other units, other tasks, other names — and the rules would not change. The table shows that the mechanism can be written down for a particular world, which is a different claim from saying the mechanism is that table.

## What follows from the principles

- The number of levels is a consequence, not a decision. It follows from the population, the address space, the plenum size and the branching, and it changes when those change.
- The number of seats follows from membership, not from a resolution. A council has as many seats as it has acceding councils — no more and no fewer. Nobody apportions seats, because there is nothing to apportion.
- Continents and nations have no special status. A continental council is a council like any other that happens to be a continent. If people constitute a nation as a council, it is a council; if they do not, the nation is not a level of the cascade.
- If a council grows too large to work, that is a signal that an intermediate level is missing, not a reason to cap the number of members. Capping hides the problem; adding the missing level solves it, and the same rule then applies to the new level as to every other.

## Open questions

This is a first draft, and these are the points it does not settle.

- **Verifying identity across the whole chain.** The framework requires the delegation chain to be verifiable end to end, but not how the Web of Trust does this in practice — what a person must present, what a neighbourhood can attest, how attestation survives at scale without becoming a registry.
- **Withdrawing accession.** Accession brings a council into being at the level above. How a council leaves an upper council again — and what happens to the upper council if enough councils leave — is not defined. Withdrawal cannot be impossible, or accession is a trap; it cannot be free, or the cascade is unstable.
- **Dissolving committees.** Committees are established by decision of councils. By what decision they end, and who inherits their tasks and records when they do, is not defined here.
- **Amending the invariants.** Human rights and the ecological ceiling are the condition of recognition, not the property of a top level. But they must be amendable in some way, or the framework fixes the moral horizon of every future generation. How they are amended without creating a body that can amend everything is the hardest question in this document. It is left open rather than answered badly.
