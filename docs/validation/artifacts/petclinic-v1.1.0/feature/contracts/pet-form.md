# Existing Pet Form Boundary

No new endpoint is introduced. Existing create/update POST routes under
`/owners/{ownerId}/pets` continue binding Pet and reporting birthDate errors
through BindingResult and the existing pet form. The shared validator now rejects
a future LocalDate directly using `typeMismatch.birthDate`. Missing dates retain
`required`; valid dates, routes, redirects, duplicate handling, and templates
remain unchanged.
