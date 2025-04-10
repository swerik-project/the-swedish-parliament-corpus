# Add speech IDs and a `<composition>` element to metadata

## Status

proposed

## Context

There are two issues that have been under discussion for some time:

1. How can we assign and store IDs for individual speeches in a parlaclarin-compliant structure?
2. How can we implement labelling / tagging parts of the documents in a way that is flexible enough to handle inherently messy data and non-hierarchical / discontiguous / overlapping structures under the iterative work flows we use while remaining parlaclarin compliant?

## Decision

### TLDR

- add `<composition>` element to TEI header
- "speech": a "speech" is spoken by a person from their introduction to another intro or subsequent order of business
- IDs of `<composition>` element children change when the content of the pointers the child element references change

### Adding an element

Add the `<composition>` element to the TEI header. There we keep a list of speeches in `note` elements with `type="speech"` and `xml:id` attributes (1). These speech notes contain `ptr` elements that reference the IDs of `u` elements contained in the speech. Using a similar strategy we label section types in the same way (2) e.g. an interpellation debate is indicated by a note with `type="debate"` and `subtype="interpellationDebate"`; the note contains lists of pointers, e.g. to the debateSection div(s) where the debate is contained and the speech IDs of the speeches that are part of that section.


### Flexibility

The proposed strategy allows us to elaborate the text structure at any level of detail without relying on nesting or hierarchical structure imposed by XML. Meanwhile it's also TEI and Parlaclarin complient. Another advantage is that adding/removing/editing text structure descriptions or delimitation of speeches does not require edits to the corpus docs' `<body>`; all the magic happens within the TEI header.


### Minimal working example

A minimal working example is attached to the pull request associated with this decision. In the example excepts, speeches in an interpellation debate and the interpellation debate itself are reflected under the `<composition>` element.


### What is a speech?

A speech is text representing spoken language, after an introduction, by the person who was introduced, until (a) another speaker is introduced or (b) a new order of business begins (end debateSection div).


### When to change speech IDs?

When the content of a speech is changed:
1. When the introduction before the speech is not the same anymore, i.e. the introduction classification changes right before the speech
2. When the introduction after the speech is not the same anymore, i.e. the introduction classification changes right after the speech (a)
3. If the speech is terminated at a different point than before due to changed section labeling (b)

The speech ID is deterministically generated from the ID of the introduction that starts the speech, and the ID of the element (a or b) that terminates the speech. This corresponds to the rules 1-3 above.

# Why not a speech ID in the u elements

There are some reasons not to have the IDs in the `<u>` elements as attributes:
- The ParlaClarin does not have a dedicated attribute for it
- As we add different overlapping entities, the elements would get cluttered
- Accessing all speech IDs in the same place in the metadata is better in terms of usability

## Consequences

We get a parlaclarin compliant means to store speech IDs and a sufficiently flexible way to annotate structures in the protocol documents.
