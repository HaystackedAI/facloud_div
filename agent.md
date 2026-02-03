## What the “agent” must decide

Before doing vector search, the system must decide:

> **Does this question REQUIRE dividend data search, or is it a general question?**

Examples:

* “What is a dividend?” → ❌ no search
* “Which dividends are next week?” → ✅ search
* “Explain dividend yield” → ❌ no search
* “What dividend does TD Bank pay next week?” → ✅ search

This is **exactly** what interviewers mean by *agentic framework* .


## 2.1 Agent decision contract

### Input

User question

### Output

<pre class="overflow-visible! px-0!" data-start="953" data-end="1036"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-json"><span><span><span class="hljs-punctuation">{</span></span><span>
  </span><span><span class="hljs-attr">"action"</span></span><span><span class="hljs-punctuation">:</span></span><span> </span><span><span class="hljs-string">"search"</span></span><span> | </span><span><span class="hljs-string">"no_search"</span></span><span><span class="hljs-punctuation">,</span></span><span>
  </span><span><span class="hljs-attr">"reason"</span></span><span><span class="hljs-punctuation">:</span></span><span> </span><span><span class="hljs-string">"short explanation"</span></span><span>
</span><span><span class="hljs-punctuation">}</span></span><span>
</span></span></code></div></div></pre>
