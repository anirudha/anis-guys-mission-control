/// <reference types="cypress" />

describe("/activity feed", () => {
  const apiBase = "**/api/v1";

  function stubStreamEmpty() {
    cy.intercept(
      "GET",
      `${apiBase}/activity/task-comments/stream*`,
      {
        statusCode: 200,
        headers: {
          "content-type": "text/event-stream",
        },
        body: "",
      },
    ).as("activityStream");
  }

  function signInWithClerk({ otp }: { otp: string }) {
    cy.contains(/sign in to view the feed/i).should("be.visible");
    cy.get('[data-testid="activity-signin"]').click();

    // Redirect mode should bring us to a full-page Clerk sign-in experience.
    cy.get('input[type="email"], input[name="identifier"]', { timeout: 20_000 })
      .first()
      .should("be.visible")
      .clear()
      .type("jane+clerk_test@example.com");

    cy.contains('button', /continue|sign in/i).click();

    cy.get('input', { timeout: 20_000 })
      .filter('[inputmode="numeric"], [autocomplete="one-time-code"], [type="tel"], [name="code"], [type="text"]')
      .first()
      .should("be.visible")
      .type(otp);

    cy.contains('button', /verify|continue|sign in/i).click();

    // Back to app
    cy.contains(/live feed/i, { timeout: 30_000 }).should("be.visible");
  }

<<<<<<< HEAD
=======
  
>>>>>>> a6188f5 (test(e2e): add negative auth case (wrong OTP))
  it("auth negative: wrong OTP shows an error", () => {
    cy.visit("/activity");

    cy.contains(/sign in to view the feed/i).should("be.visible");
    cy.get('[data-testid="activity-signin"]').click();

<<<<<<< HEAD
    cy.get('input[type="email"], input[name="identifier"]', { timeout: 20_000 })
      .first()
      .should("be.visible")
      .clear()
      .type("jane+clerk_test@example.com");

    cy.contains('button', /continue|sign in/i).click();

    cy.get('input', { timeout: 20_000 })
      .filter('[inputmode="numeric"], [autocomplete="one-time-code"], [type="tel"], [name="code"], [type="text"]')
      .first()
      .should("be.visible")
      .type("000000");

    cy.contains('button', /verify|continue|sign in/i).click();

    cy.contains(/invalid|incorrect|try again/i, { timeout: 20_000 }).should("be.visible");
=======
    cy.contains(/email address/i).should("be.visible");
    cy.get('input[type="email"]').clear().type("jane+clerk_test@example.com");
    cy.contains(/continue|sign in/i).click();

    cy.contains(/verification code|code/i).should("be.visible");
    // Wrong code
    cy.get('input')
      .filter('[inputmode="numeric"], [autocomplete="one-time-code"], [type="tel"], [type="text"]')
      .first()
      .type("000000");

    // Clerk should display an error message.
    cy.contains(/invalid|incorrect|try again/i).should("be.visible");
>>>>>>> a6188f5 (test(e2e): add negative auth case (wrong OTP))
  });

  it("happy path: renders task comment cards", () => {
    cy.intercept("GET", `${apiBase}/activity/task-comments*`, {
      statusCode: 200,
      body: {
        items: [
          {
            id: "c1",
            message: "Hello world",
            agent_name: "Kunal",
            agent_role: "QA 2",
            board_id: "b1",
            board_name: "Testing",
            task_id: "t1",
            task_title: "CI hardening",
            created_at: "2026-02-07T00:00:00Z",
          },
        ],
      },
    }).as("activityList");

    stubStreamEmpty();

    cy.visit("/activity");
    signInWithClerk({ otp: "424242" });

    cy.wait("@activityList");
    cy.contains("CI hardening").should("be.visible");
    cy.contains("Hello world").should("be.visible");
  });

  it("empty state: shows waiting message when no items", () => {
    cy.intercept("GET", `${apiBase}/activity/task-comments*`, {
      statusCode: 200,
      body: { items: [] },
    }).as("activityList");

    stubStreamEmpty();

    cy.visit("/activity");
    signInWithClerk({ otp: "424242" });

    cy.wait("@activityList");
    cy.contains(/waiting for new comments/i).should("be.visible");
  });

  it("error state: shows failure UI when API errors", () => {
    cy.intercept("GET", `${apiBase}/activity/task-comments*`, {
      statusCode: 500,
      body: { detail: "boom" },
    }).as("activityList");

    stubStreamEmpty();

    cy.visit("/activity");
    signInWithClerk({ otp: "424242" });

    cy.wait("@activityList");
    cy.contains(/unable to load feed|boom/i).should("be.visible");
  });
});
