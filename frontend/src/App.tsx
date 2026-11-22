
import { useEffect, useState } from "react";
import {
  api,
  type ProfileInput,
  type Skill,
  type SkillInput,
} from "./services/api";
import "./App.css";

const emptyProfile: ProfileInput = {
  name: "",
  role: "",
  experience_years: 0,
  target_company: "",
};

const emptySkill: SkillInput = {
  name: "",
  level: "Intermediate",
  priority: "Medium",
};

function App() {
  const [profile, setProfile] =
    useState<ProfileInput>(emptyProfile);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [skill, setSkill] =
    useState<SkillInput>(emptySkill);
  const [hasProfile, setHasProfile] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const saved = await api.getProfile();
        setProfile(saved);
        setHasProfile(true);
        setSkills(await api.getSkills());
      } catch (error) {
        if (
          error instanceof Error &&
          !error.message.includes("Create your profile first")
        ) {
          setMessage(error.message);
        }
      }
    }

    void load();
  }, []);

  async function saveProfile(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);

    try {
      await api.saveProfile(profile);
      setHasProfile(true);
      setMessage("Profile saved successfully");
      setSkills(await api.getSkills());
    } catch (error) {
      setMessage(String(error));
    } finally {
      setBusy(false);
    }
  }

  async function addSkill(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);

    try {
      const created = await api.addSkill(skill);
      setSkills((current) => [...current, created]);
      setSkill(emptySkill);
      setMessage("Skill added");
    } catch (error) {
      setMessage(String(error));
    } finally {
      setBusy(false);
    }
  }

  async function deleteSkill(id: number) {
    setBusy(true);

    try {
      await api.deleteSkill(id);
      setSkills((current) =>
        current.filter((item) => item.id !== id)
      );
      setMessage("Skill deleted");
    } catch (error) {
      setMessage(String(error));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">✦ InterviewGenie</div>
        <span className="version">Sprint 1 · Foundation</span>
      </header>

      <main className="container">
        <section className="intro">
          <span className="eyebrow">YOUR AI CAREER COACH</span>
          <h1>Prepare for your next big opportunity.</h1>
          <p>
            Personalize your interview preparation.
            Add your profile and skills to get started.
          </p>
        </section>

        {message && (
          <div className="message" role="status">
            {message}
          </div>
        )}

        <div className="layout">
          <section className="panel">
            <h2>Interview Profile</h2>
            <p className="muted">
              Tell us about your experience and target role.
            </p>

            <form onSubmit={saveProfile}>
              <label>Full name</label>
              <input
                required
                value={profile.name}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    name: e.target.value,
                  })
                }
                placeholder="Your name"
              />

              <label>Target role</label>
              <input
                required
                value={profile.role}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    role: e.target.value,
                  })
                }
                placeholder="Senior Software Engineer"
              />

              <label>Years of experience</label>
              <input
                required
                type="number"
                min="0"
                max="60"
                value={profile.experience_years}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    experience_years: Number(e.target.value),
                  })
                }
              />

              <label>Target company</label>
              <input
                required
                value={profile.target_company}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    target_company: e.target.value,
                  })
                }
                placeholder="Google, Microsoft, Amazon..."
              />

              <button disabled={busy} type="submit">
                Save Profile
              </button>
            </form>
          </section>

          <section className="panel">
            <h2>My Skills</h2>
            <p className="muted">
              Choose the areas you want to practice.
            </p>

            <form onSubmit={addSkill}>
              <label>Skill name</label>
              <input
                required
                value={skill.name}
                onChange={(e) =>
                  setSkill({
                    ...skill,
                    name: e.target.value,
                  })
                }
                placeholder="Python, Java, System Design..."
              />

              <label>Proficiency</label>
              <select
                value={skill.level}
                onChange={(e) =>
                  setSkill({
                    ...skill,
                    level: e.target.value as SkillInput["level"],
                  })
                }
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>

              <label>Interview priority</label>
              <select
                value={skill.priority}
                onChange={(e) =>
                  setSkill({
                    ...skill,
                    priority: e.target.value as SkillInput["priority"],
                  })
                }
              >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>

              <button disabled={busy || !hasProfile}>
                Add Skill
              </button>

              {!hasProfile && (
                <p className="muted">
                  Save your profile before adding skills.
                </p>
              )}
            </form>

            <div className="skills">
              {skills.map((item) => (
                <div className="skill" key={item.id}>
                  <div>
                    <strong>{item.name}</strong>
                    <small>
                      {item.level} · {item.priority} priority
                    </small>
                  </div>
                  <button
                    className="delete"
                    disabled={busy}
                    onClick={() => deleteSkill(item.id)}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
