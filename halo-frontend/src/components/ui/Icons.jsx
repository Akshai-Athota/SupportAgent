/**
 * Inline SVG icon set. Each accepts size + any svg props.
 * No emoji / decorative illustration — clean line + the brand spark.
 */
const base = (size) => ({
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
});

export function Spark({ size = 20, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M12 3l1.9 5.5L19.5 10l-5.6 1.5L12 17l-1.9-5.5L4.5 10l5.6-1.5L12 3z"
        fill={color}
      />
    </svg>
  );
}

export function Plus({ size = 16, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path d="M12 5v14M5 12h14" stroke={color} strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function Send({ size = 18, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M12 19V5M5 12l7-7 7 7"
        stroke={color}
        strokeWidth="2.3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Trash({ size = 14, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M4 7h16M9 7V5h6v2M7 7l1 13h8l1-13"
        stroke={color}
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function ChatBubble({ size = 15, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5z"
        stroke={color}
        strokeWidth="1.7"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Logout({ size = 16, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"
        stroke={color}
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Chevron({ size = 16, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M8 9l4-4 4 4M8 15l4 4 4-4"
        stroke={color}
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function Check({ size = 11, color = "currentColor", ...props }) {
  return (
    <svg {...base(size)} {...props}>
      <path
        d="M20 6L9 17l-5-5"
        stroke={color}
        strokeWidth="2.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
